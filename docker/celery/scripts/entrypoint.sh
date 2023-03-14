#!/bin/sh
set -e

/scripts/start.sh

exec "$@"
