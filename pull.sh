#!/bin/bash

git pull

SERVICE=django_cmc

echo -e "Restart Service" $SERVICE

exec supervisorctl  restart $SERVICE
