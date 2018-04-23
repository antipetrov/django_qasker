#!/bin/bash

export DJANGO_SETTINGS_MODULE=hasker.settings_docker

mysql -h mysql -u root -proot < init.sql

uwsgi --ini /opt/hasker/uwsgi.ini