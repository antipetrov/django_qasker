#!/bin/bash

export DJANGO_SETTINGS_MODULE=hasker.settings_docker

mysql -h mysql -u root -proot < init.sql

python manage.py migrate

python manage.py collectstatic


uwsgi --ini /opt/hasker/uwsgi.ini