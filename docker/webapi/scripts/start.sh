#!/bin/sh
export FLASK_DEBUG=1
python -m flask db upgrade
python -m manage

#gunicorn -b $APP_HOST:$APP_PORT -w 4 wsgi:app
