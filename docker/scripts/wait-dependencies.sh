#!/bin/sh
set -e

# Postgres
echo "\033[94mWaiting the service: \033[97mPostgres (url=$POSTGRES_HOST:$POSTGRES_PORT)\033[00m"
/scripts/wait-for-it.sh $POSTGRES_HOST:$POSTGRES_PORT -t 120 --
echo "\033[01;32mPostgres is up!\033[00m"

# Redis
echo "\033[94mWaiting the service: \033[97mRedis (url=$REDIS_HOST:$REDIS_PORT)\033[00m"
/scripts/wait-for-it.sh $REDIS_HOST:$REDIS_PORT -t 120 --
echo "\033[01;32mRedis is up!\033[00m"
echo ""

exec "$@"
