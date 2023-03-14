#!/bin/sh
celery -A config.celery beat -l info