# Mo Tech test

this is a test for Mo Tech company

### create a super user

```bash
docker-compose run django_backend python /app/src/manage.py createsuperuser
```

### run the project

```bash
docker-compose up --build
```

### run the tests

```bash
docker-compose run django_backend python /app/src/manage.py test
```

or you can run the bash

```bash
./test
```
