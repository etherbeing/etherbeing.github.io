#!/bin/sh

ROOT_DIRECTORY=$(pwd)
TMP_PIDS=$ROOT_DIRECTORY/.temp
API_DIRECTORY=$ROOT_DIRECTORY/api/
REDIS_SERVER_DATA=/tmp/redis/

mkdir -p $TMP_PIDS
mkdir -p $REDIS_SERVER_DATA

cleanup() {
    trap - EXIT HUP INT TERM
    kill $(cat $REDIS_PID)
    kill $(cat $API_PID)
    kill $(cat $WEB_PID)
    
    rm $TMP_PIDS/*
    rmdir $TMP_PIDS
    if [ "$POSTGRES_RUNNING" -ne 0 ]; then
        systemctl stop postgresql
    fi
    exit 0
}

handle_sigint() {
    echo "Received SIGINT signal, quitting now gratefully..."
    cleanup
}

trap 'handle_sigint' EXIT HUP INT TERM

# PostgreSQL
1>/dev/null systemctl status postgresql
POSTGRES_RUNNING=$?
if [ "$POSTGRES_RUNNING" -ne 0 ]; then
    systemctl start postgresql
fi

# Run redis cache server
REDIS_PID=$TMP_PIDS/redis.pid
cd $REDIS_SERVER_DATA
redis-server &
echo $! > $REDIS_PID

# API server
API_PID=$TMP_PIDS/api.pid
cd $API_DIRECTORY
uv run src/etherbeing/manage.py runserver &
echo $! > $API_PID

# Frontend server
WEB_PID=$TMP_PIDS/web.pid
cd $ROOT_DIRECTORY
pnpm run dev &
echo $! > $WEB_PID

echo "Services are now up and running, now waiting for them to die (NOTE that killing the frontend pid is enough to kill them all)"
echo REDIS pid: $(cat $REDIS_PID)
echo API pid: $(cat $API_PID)
echo WEB pid: $(cat $WEB_PID)

wait $(cat $WEB_PID)

cleanup