#!/bin/sh
#
# Initializes a gunicorn-django container
#



WEB_APP=cmc
: ${WEB_APP_PORT:=80}
: ${WEB_APP_WORKERS:=2}

set -e

echo "start django website:$WEB_APP at port:$WEB_APP_PORT"



python manage.py migrate
python manage.py collectstatic --noinput
gunicorn $WEB_APP.wsgi:application -w $WEB_APP_WORKERS -b 0.0.0.0:$WEB_APP_PORT

