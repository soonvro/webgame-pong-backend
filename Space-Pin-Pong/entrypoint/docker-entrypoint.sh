#!/bin/sh

echo "+_+| Running Database Migrations"
python manage.py makemigrations
python manage.py migrate

SCRIPT_DIRECTORY="$(dirname $(realpath "$0"))"
/bin/sh $SCRIPT_DIRECTORY/docker-entrypoint.${DJANGO_ENV}.sh

exec "$@"
