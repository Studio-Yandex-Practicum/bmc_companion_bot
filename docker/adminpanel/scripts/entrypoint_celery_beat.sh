#!/bin/sh
set -e

/scripts/wait-dependencies.sh
/scripts/start_celery_beat.sh

exec "$@"