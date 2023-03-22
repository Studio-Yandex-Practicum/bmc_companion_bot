#!/bin/sh
set -e

/scripts/wait-dependencies.sh
/scripts/start.sh

exec "$@"
