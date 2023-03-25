#!/bin/sh
set -e

/scripts/start_adminpanel.sh

exec "$@"
