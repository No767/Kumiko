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
# Blue Alliance
if [[ -v BLUE_ALLIANCE_API_KEY ]]; then
    echo "Blue_Alliance_API_Key=${BLUE_ALLIANCE_API_KEY}" >> /Kumiko/Bot/.env
else
    echo "Missing Blue Alliance API key! BLUE_ALLIANCE_API_KEY environment variable is not set."
fi 
# Discord
if [[ -v DISCORD_BOTS_API_KEY ]]; then
    echo "Discord_Bots_API_Key=${DISCORD_BOTS_API_KEY}" >> /Kumiko/Bot/.env
else
    echo "Missing Discord Bots API key! DISCORD_BOTS_API_KEY environment variable is not set."
fi 
# First Events
if [[ -v FIRST_EVENTS_FINAL_KEY ]]; then
    echo "FIRST_Events_Final_Key=${FIRST_EVENTS_FINAL_KEY}" >> /Kumiko/Bot/.env
else
    echo "Missing First Events Final key! FIRST_EVENTS_FINAL_KEY environment variable is not set."
fi 
# GitHub
if [[ -v GITHUB_API_ACCESS_TOKEN ]]; then
    echo "GitHub_API_Access_Token=${GITHUB_API_ACCESS_TOKEN}" >> /Kumiko/Bot/.env
else
    echo "Missing GitHub API token! GITHUB_API_ACCESS_TOKEN environment variable is not set."
fi 
# Hypixel
if [[ -v HYPIXEL_API_KEY ]]; then
    echo "Hypixel_API_Key=${HYPIXEL_API_KEY}" >> /Kumiko/Bot/.env
else
    echo "Missing Hypixel API key! HYPIXEL_API_KEY environment variable is not set."
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
# Top GG
if [[ -v TOP_GG_API_KEY ]]; then
    echo "Top_GG_API_Key=${TOP_GG_API_KEY}" >> /Kumiko/Bot/.env
else
    echo "Missing Top GG API key! TOP_GG_API_KEY environment variable is not set."
fi
# Twitch access token
if [[ -v TWITCH_API_ACCESS_TOKEN ]]; then
    echo "Twitch_API_Access_Token=${TWITCH_API_ACCESS_TOKEN}" >> /Kumiko/Bot/.env
else
    echo "Missing Twitch API access token! TWITCH_API_ACCESS_TOKEN environment variable is not set."
fi
# Twitch client ID
if [[ -v TWITCH_API_CLIENT_ID ]]; then
    echo "Twitch_API_Client_ID=${TWITCH_API_CLIENT_ID}" >> /Kumiko/Bot/.env
else
    echo "Missing Twitch API client id! TWITCH_API_CLIENT_ID environment variable is not set."
fi
# Twitter
if [[ -v TWITTER_BEARER_TOKEN ]]; then
    echo "Twitter_Bearer_Token=${TWITTER_BEARER_TOKEN}" >> /Kumiko/Bot/.env
else
    echo "Missing Twitter bearer token! TWITTER_BEARER_TOKEN environment variable is not set."
fi
# YouTube
if [[ -v YOUTUBE_API_KEY ]]; then
    echo "YouTube_API_Key=${YOUTUBE_API_KEY}" >> /Kumiko/Bot/.env
else
    echo "Missing YouTube API key! YOUTUBE_API_KEY environment variable is not set."
fi

if [[ -v POSTGRES_PASSWORD ]]; then
    echo "Postgres_Password_Dev=${POSTGRES_PASSWORD}" >> /Kumiko/Bot/.env
else
    echo "Missing Postgres_Password env var! Postgres_Password environment variable is not set."
    exit 1;
fi

if [[ -v POSTGRES_USERNAME ]]; then
    echo "Postgres_Username_Dev=${POSTGRES_USERNAME}" >> /Kumiko/Bot/.env
else
    echo "Missing Postgres_Username env var! Postgres_Username_Dev environment variable is not set."
    exit 1;
fi

if [[ -v POSTGRES_IP ]]; then
    echo "Postgres_Server_IP_Dev=${POSTGRES_IP}" >> /Kumiko/Bot/.env
else
    echo "Missing Postgres_Server_IP_Dev env var! Postgres_Server_IP_Dev environment variable is not set."
    exit 1;
fi

if [[ -v POSTGRES_PORT ]]; then
    echo "Postgres_Port_Dev=${POSTGRES_PORT}" >> /Kumiko/Bot/.env
else
    echo "Missing Postgres_Port_Dev env var! Postgres_Port_Dev environment variable is not set."
    exit 1;
fi

if [[ -v POSTGRES_ECO_USERS_DB ]]; then
    echo "Postgres_Database_Dev=${POSTGRES_ECO_USERS_DB}" >> /Kumiko/Bot/.env
else
    echo "Missing Postgres_Database_Dev env var! Postgres_Database_Dev environment variable is not set."
    exit 1;
fi

if [[ -v POSTGRES_WS_DB ]]; then
    echo "Postgres_Wish_Sim_Database=${POSTGRES_WS_DB}" >> /Kumiko/Bot/.env
else
    echo "Missing Postgres_Wish_Sim_Database env var! Postgres_Wish_Sim_Database environment variable is not set."
    exit 1;
fi

if [[ -v POSTGRES_AH_DB ]]; then
    echo "Postgres_Database_AH_Dev=${POSTGRES_AH_DB}" >> /Kumiko/Bot/.env
else
    echo "Missing Postgres_Database_AH_Dev env var! Postgres_Database_AH_Dev environment variable is not set."
    exit 1;
fi

if [[ -v POSTGRES_QUESTS_DB ]]; then
    echo "Postgres_Quests_Database=${POSTGRES_QUESTS_DB}" >> /Kumiko/Bot/.env
else
    echo "Missing Postgres_Quests_Database env var! Postgres_Quests_Database environment variable is not set."
    exit 1;
fi

if [[ -v MONGODB_PASSWORD ]]; then
    echo "MongoDB_Password_Dev=${MONGODB_PASSWORD}" >> /Kumiko/Bot/.env
else
    echo "Missing MongoDB_Password_Dev env var! MongoDB_Password_Dev environment variable is not set."
    exit 1;
fi

if [[ -v MONGODB_USER ]]; then
    echo "MongoDB_Username_Dev=${MONGODB_USER}" >> /Kumiko/Bot/.env
else
    echo "Missing MongoDB_Username_Dev env var! MongoDB_Username_Dev environment variable is not set."
    exit 1;
fi

if [[ -v MONGODB_IP ]]; then
    echo "MongoDB_Server_IP_Dev=${MONGODB_IP}" >> /Kumiko/Bot/.env
else
    echo "Missing MongoDB_Server_IP_Dev env var! MongoDB_Server_IP_Dev environment variable is not set."
    exit 1;
fi

if [[ -v MONGODB_PORT ]]; then
    echo "MongoDB_Server_Port_Dev=${MONGODB_PORT}" >> /Kumiko/Bot/.env
else
    echo "Missing MongoDB_Server_Port_Dev env var! MongoDB_Server_Port_Dev environment variable is not set."
    exit 1;
fi

if [[ -v RABBITMQ_PASSWORD ]]; then
    echo "RabbitMQ_Password_Dev=${RABBITMQ_PASSWORD}" >> /Kumiko/Bot/.env
else
    echo "Missing RabbitMQ_Password_Dev env var! RabbitMQ_Password_Dev environment variable is not set."
    exit 1;
fi

if [[ -v RABBITMQ_USER ]]; then
    echo "RabbitMQ_Username_Dev=${RABBITMQ_USER}" >> /Kumiko/Bot/.env
else
    echo "Missing RabbitMQ_Username_Dev env var! RabbitMQ_Username_Dev environment variable is not set."
    exit 1;
fi

if [[ -v RABBITMQ_IP ]]; then
    echo "RabbitMQ_Server_IP_Dev=${RABBITMQ_IP}" >> /Kumiko/Bot/.env
else
    echo "Missing RabbitMQ_Server_IP_Dev env var! RabbitMQ_Server_IP_Dev environment variable is not set."
    exit 1;
fi

if [[ -v RABBITMQ_PORT ]]; then
    echo "RabbitMQ_Port_Dev=${RABBITMQ_PORT}" >> /Kumiko/Bot/.env
else
    echo "Missing RabbitMQ_Port_Dev env var! RabbitMQ_Port_Dev environment variable is not set."
    exit 1;
fi

if [[ -v REDIS_IP ]]; then
    echo "Redis_Server_IP_Dev=${REDIS_IP}" >> /Kumiko/Bot/.env
else
    echo "Missing Redis_Server_IP_Dev env var! Redis_Server_IP_Dev environment variable is not set."
    exit 1;
fi

if [[ -v REDIS_PORT ]]; then
    echo "Redis_Port_Dev=${REDIS_PORT}" >> /Kumiko/Bot/.env
else
    echo "Missing Redis_Port_Dev env var! Redis_Port_Dev environment variable is not set."
    exit 1;
fi

exec python3 /Kumiko/Bot/kumikobot.py