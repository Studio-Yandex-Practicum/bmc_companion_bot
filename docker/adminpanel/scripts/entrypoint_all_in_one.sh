#!/bin/bash

/scripts/entrypoint_adminpanel.sh &
/scripts/entrypoint_celery.sh &
/scripts/entrypoint_celery_beat.sh &

# Wait for any process to exit
wait -n

# Exit with status of process that exited first
exit $?
