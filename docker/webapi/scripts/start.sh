#!/bin/sh
python -m flask db upgrade
gunicorn -b $APP_HOST:$APP_PORT -w 4 wsgi:app
