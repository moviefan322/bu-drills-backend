#!/bin/sh

set -e

python manage.py wait_for_db
python manage.py migrate
python manage.py run_seeds

uwsgi --socket :9000 --master --enable-threads --module app.wsgi