#!/bin/bash

source /home/www/venvs/mynota/bin/activate
cd /home/www/sites/mynota_python
python manage.py collectstatic  #Comando apenas se existir mais de uma app no projeto
gunicorn mynota_python.wsgi:application -b 127.0.0.1:9001 -D

