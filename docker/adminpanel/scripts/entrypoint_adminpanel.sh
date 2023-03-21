#!/bin/sh
set -e

/scripts/wait-dependencies.sh
/scripts/start_adminpanel.sh

exec "$@"