#!/bin/bash

NAME="cmc.website"                                  # Name of the application
DJANGODIR=/opt/cmc.website/deploy                 # Django project directory
SOCKFILE=/opt/cmc.website/tmp/cmc.website.sock                                                 # we will communicte using this unix socket
USER=root                                      # the user to run as
GROUP=root                                    # the group to run as
NUM_WORKERS=1                                   # how many worker processes should Gunicorn spawn
DJANGO_SETTINGS_MODULE=cmc.settings            # which settings file should Django use
DJANGO_WSGI_MODULE=cmc.wsgi                     # WSGI module name
LOGFILE=/opt/cmc.website/logs/gunicorn.log
TIMEOUT=30
echo "Starting $NAME"

# Activate the virtual environment
cd $DJANGODIR
source /opt/cmc.website/venv/bin/activate
export DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE
export PYTHONPATH=$DJANGODIR:$PYTHONPATH

# Create the run directory if it doesn't exist
RUNDIR=$(dirname $SOCKFILE)
test -d $RUNDIR || mkdir -p $RUNDIR

# Start your Django Unicorn
# Programs meant to be run under supervisor should not daemonize themselves (do not use --daemon)
echo "!!!!!!!!"

python manage.py migrate
python manage.py collectstatic --noinput
#python manage.py runserver 0.0.0.0:80


exec gunicorn ${DJANGO_WSGI_MODULE}:application --name $NAME --workers $NUM_WORKERS --timeout $TIMEOUT --user=$USER --group=$GROUP --log-level=debug --bind=0.0.0.0:80 --log-file=$LOGFILE
