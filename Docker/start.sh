#!/usr/bin/env bash

KUMIKO_FIRST_START_CHECK="KUMIKO_FIRST_START"

if [ ! -f $KUMIKO_FIRST_START_CHECK ]; then
    touch $KUMIKO_FIRST_START_CHECK
    echo 'DO NOT EDIT THIS FILE! THIS IS USED WHEN YOU FIRST RUN KUMIKO USING DOCKER!' >> $KUMIKO_FIRST_START_CHECK
    exec python3 /Kumiko/migrations-runner.py
fi

exec python3 /Kumiko/Bot/kumikobot.py