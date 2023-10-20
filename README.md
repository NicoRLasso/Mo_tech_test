# Mo Tech test

this is a test for Mo Technology company

## How to run the project

### clone the project

```bash
git clone git@github.com:NicoRLasso/Mo_tech_test.git
```

### create a .env file

```bash
cp .env.example .env
```

### build the project

```bash
docker-compose build
```

### run the project

```bash
docker-compose up
```

### create a super user

```bash
docker-compose run django_backend python /app/src/manage.py createsuperuser
```

### go to swagger documentation

```bash
http://localhost:8000/api/docs
```

### run the tests

```bash
docker-compose run django_backend python /app/src/manage.py test
```

or you can run the bash

```bash
./test
```
