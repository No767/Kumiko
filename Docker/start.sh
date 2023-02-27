#!/usr/bin/env bash

if [[ -v KUMIKO_TOKEN ]]; then
    echo "Kumiko_Token=${KUMIKO_TOKEN}" >> /Kumiko/Bot/.env
else
    echo "Missing Kumiko's bot token! KUMIKO_TOKEN environment variable is not set."
    exit 1;
fi

# Testing bot token
# Not needed in production
if [[ -v DEV_BOT_TOKEN ]]; then
    echo "Dev_Bot_Token=${DEV_BOT_TOKEN}" >> /Kumiko/Bot/.env
fi 

# API Keys
# GitHub
if [[ -v GITHUB_API_ACCESS_TOKEN ]]; then
    echo "GitHub_API_Access_Token=${GITHUB_API_ACCESS_TOKEN}" >> /Kumiko/Bot/.env
else
    echo "Missing GitHub API token! GITHUB_API_ACCESS_TOKEN environment variable is not set."
fi 
# Reddit ID
if [[ -v REDDIT_ID ]]; then
    echo "Reddit_ID=${REDDIT_ID}" >> /Kumiko/Bot/.env
else
    echo "Missing Reddit ID! REDDIT_ID environment variable is not set."
fi 
# Reddit Secret
if [[ -v REDDIT_SECRET ]]; then
    echo "Reddit_Secret=${REDDIT_SECRET}" >> /Kumiko/Bot/.env
else
    echo "Missing Reddit secret! REDDIT_SECRET environment variable is not set."
fi 
# Tenor
if [[ -v TENOR_API_KEY ]]; then
    echo "Kumiko_Tenor_API_Key=${TENOR_API_KEY}" >> /Kumiko/Bot/.env
else
    echo "Missing Tenor API key! TENOR_API_KEY environment variable is not set."
fi 
# YouTube

if [[ -v IPC_SECRET_KEY ]]; then
    echo "IPC_Secret_Key=${IPC_SECRET_KEY}" >> /Kumiko/Bot/.env
else
    echo "Missing IPC_Secret_Key env var! IPC_Secret_Key environment variable is not set."
    exit 1;
fi

if [[ -v DATABASE_URL ]]; then
    echo "DATABASE_URL=${DATABASE_URL}" >> /Kumiko/.env
else
    echo "Missing DATABASE_URL env var! DATABASE_URL environment variable is not set."
    exit 1;
fi

### Not really needed anymore
if [[ -v POSTGRES_PASSWORD ]]; then
    echo "Postgres_Password=${POSTGRES_PASSWORD}" >> /Kumiko/Bot/.env
else
    echo "Missing Postgres_Password env var! Postgres_Password environment variable is not set."
    exit 1;
fi

if [[ -v POSTGRES_USER ]]; then
    echo "Postgres_Username=${POSTGRES_USER}" >> /Kumiko/Bot/.env
else
    echo "Missing Postgres_Username env var! Postgres_Username_Dev environment variable is not set."
    exit 1;
fi

if [[ -v POSTGRES_IP ]]; then
    echo "Postgres_Server_IP=${POSTGRES_IP}" >> /Kumiko/Bot/.env
else
    echo "Missing Postgres_Server_IP env var! Postgres_Server_IP environment variable is not set."
    exit 1;
fi

if [[ -v POSTGRES_PORT ]]; then
    echo "Postgres_Port=${POSTGRES_PORT}" >> /Kumiko/Bot/.env
else
    echo "Missing Postgres_Port env var! Postgres_Port environment variable is not set."
    exit 1;
fi

if [[ -v POSTGRES_KUMIKO_DB ]]; then
    echo "Postgres_Kumiko_Database=${POSTGRES_KUMIKO_DB}" >> /Kumiko/Bot/.env
else
    echo "Missing Postgres_Kumiko_Database env var! Postgres_Kumiko_Database environment variable is not set."
    exit 1;
fi
###

if [[ -v REDIS_IP ]]; then
    echo "Redis_Server_IP=${REDIS_IP}" >> /Kumiko/Bot/.env
else
    echo "Missing Redis_Server_IP env var! Redis_Server_IP environment variable is not set."
    exit 1;
fi

if [[ -v REDIS_PORT ]]; then
    echo "Redis_Port=${REDIS_PORT}" >> /Kumiko/Bot/.env
else
    echo "Missing Redis_Port env var! Redis_Port environment variable is not set."
    exit 1;
fi

KUMIKO_FIRST_START_CHECK="KUMIKO_FIRST_START"

if [ ! -f $KUMIKO_FIRST_START_CHECK ]; then
    touch $KUMIKO_FIRST_START_CHECK
    echo 'DO NOT EDIT THIS FILE! THIS IS USED WHEN YOU FIRST RUN KUMIKO USING DOCKER!' >> $KUMIKO_FIRST_START_CHECK
    python3 /Kumiko/init-db.py
fi

exec python3 /Kumiko/Bot/kumikobot.py