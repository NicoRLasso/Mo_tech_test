FROM python:3.11-slim-buster

# Update and install system dependencies
RUN apt-get update -qq && apt-get install -y -qq \
    gdal-bin binutils libproj-dev libgdal-dev cmake &&\
    apt-get clean all &&\
    rm -rf /var/apt/lists/* &&\
    rm -rf /var/cache/apt/*

ENV PYTHONUNBUFFERED 1

WORKDIR /app

# Copy only Pipfile and Pipfile.lock to leverage Docker cache
COPY Pipfile Pipfile.lock /app/

# Install pipenv and project dependencies
RUN pip install pipenv && \
    pipenv install --deploy --ignore-pipfile

# Copy the rest of the project
COPY . /app/

# Set execute permissions on the entry script
RUN chmod +x /app/entrypoint.sh
