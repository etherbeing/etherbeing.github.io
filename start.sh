#!/bin/sh

ROOT_DIRECTORY=$(pwd)
TMP_PIDS=$ROOT_DIRECTORY/.temp
API_DIRECTORY=$ROOT_DIRECTORY/api/
REDIS_SERVER_DATA=/tmp/redis/

mkdir -p $TMP_PIDS
mkdir -p $REDIS_SERVER_DATA

systemctl status postgresql
POSTGRES_RUNNING=$?
if ["$POSTGRES_RUNNING" -ne 0 ]; then
    systemctl start postgresql
fi
REDIS_PID=$TMP_PIDS/redis.pid
cd $REDIS_SERVER_DATA && redis-server 2>/dev/null &>$REDIS_PID
API_PID=$TMP_PIDS/api.pid
cd $API_DIRECTORY && uv run src/etherbeing/manage.py runserver &>$API_PID
WEB_PID=$TMP_PIDS/web.pid
cd $ROOT_DIRECTORY && pnpm run dev &>$WEB_PID

fg

rm $TMP_PIDS/*
rmdir $TMP_PIDS
kill $(cat $REDIS_PID)
kill $(cat $API_PID)
kill $(cat $WEb_PID)
if [ "$POSTGRES_RUNNING" -ne 0]; then
    systemctl stop postgresql
fi