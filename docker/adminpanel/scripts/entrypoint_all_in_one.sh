#!/bin/bash

/scripts/wait-dependencies.sh

/scripts/start_adminpanel.sh &
/scripts/start_celery.sh &
/scripts/start_celery_beat.sh &

# Wait for any process to exit
wait -n

# Exit with status of process that exited first
exit $?
