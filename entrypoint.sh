#!/bin/sh

echo "Running Database Migrations"
python mo_tech/manage.py makemigrations
python mo_tech/manage.py migrate

echo "Running app1 management commands"
python mo_tech/manage.py sample_management_command

exec "$@"
