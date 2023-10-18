# Define an alias for the specific Python version used in this file.
FROM python:3.11-slim-buster as python-base

# Python build stage
FROM python-base as python-build-stage

# Update and install system dependencies
RUN apt-get update -qq \
    && apt-get install -y -qq \
    gdal-bin binutils libproj-dev libgdal-dev cmake \
    # Clean up
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && rm -rf /var/cache/apt/*

# Copy only Pipfile and Pipfile.lock to leverage Docker cache
COPY Pipfile Pipfile.lock /tmp/

# Install pipenv and project dependencies
RUN pip install pipenv \
    && cd /tmp && pipenv install \
    && pipenv run pip freeze > requirements.txt \
    && pip install -r /tmp/requirements.txt


# Python 'run' stage
FROM python-base as python-run-stage

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /app/src

# Copy python dependencies from build stage
COPY --from=python-build-stage /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages

# Copy the entrypoint and start scripts and make them executable
COPY entrypoint /app/src/entrypoint
RUN sed -i 's/\r$//g' /app/src/entrypoint && chmod +x /app/src/entrypoint

COPY start /app/src/start
RUN sed -i 's/\r$//g' /app/src/start && chmod +x /app/src/start

# Copy the rest of the project
COPY . /app/src/

ENTRYPOINT ["/app/src/entrypoint"]
