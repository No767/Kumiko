#!/usr/bin/env bash

# Note that this won't be used on Kumiko. Kumiko uses a different system instead

if [[ -v TOKEN ]]; then
    echo "TOKEN=${TOKEN}" >> /Rin/Bot/.env
else
    echo "Missing bot token! TOKEN environment variable is not set."
    exit 1;
fi

# Testing bot token
# Not needed in production
if [[ -v TESTING_BOT_TOKEN ]]; then
    echo "Testing_Bot_Token=${TESTING_BOT_TOKEN}" >> /Rin/Bot/.env
fi 

# API Keys
# Blue Alliance
if [[ -v BLUE_ALLIANCE_API_KEY ]]; then
    echo "Blue_Alliance_API_Key=${BLUE_ALLIANCE_API_KEY}" >> /Rin/Bot/.env
else
    echo "Missing Blue Alliance API key! BLUE_ALLIANCE_API_KEY environment variable is not set."
fi 
# Discord
if [[ -v DISCORD_BOTS_API_KEY ]]; then
    echo "Discord_Bots_API_Key=${DISCORD_BOTS_API_KEY}" >> /Rin/Bot/.env
else
    echo "Missing Discord Bots API key! DISCORD_BOTS_API_KEY environment variable is not set."
fi 
# First Events
if [[ -v FIRST_EVENTS_FINAL_KEY ]]; then
    echo "FIRST_Events_Final_Key=${FIRST_EVENTS_FINAL_KEY}" >> /Rin/Bot/.env
else
    echo "Missing First Events Final key! FIRST_EVENTS_FINAL_KEY environment variable is not set."
fi 
# GitHub
if [[ -v GITHUB_API_ACCESS_TOKEN ]]; then
    echo "GitHub_API_Access_Token=${GITHUB_API_ACCESS_TOKEN}" >> /Rin/Bot/.env
else
    echo "Missing GitHub API token! GITHUB_API_ACCESS_TOKEN environment variable is not set."
fi 
# Hypixel
if [[ -v HYPIXEL_API_KEY ]]; then
    echo "Hypixel_API_Key=${HYPIXEL_API_KEY}" >> /Rin/Bot/.env
else
    echo "Missing Hypixel API key! HYPIXEL_API_KEY environment variable is not set."
fi 
# Reddit ID
if [[ -v REDDIT_ID ]]; then
    echo "Reddit_ID=${REDDIT_ID}" >> /Rin/Bot/.env
else
    echo "Missing Reddit ID! REDDIT_ID environment variable is not set."
fi 
# Reddit Secret
if [[ -v REDDIT_SECRET ]]; then
    echo "Reddit_Secret=${REDDIT_SECRET}" >> /Rin/Bot/.env
else
    echo "Missing Reddit secret! REDDIT_SECRET environment variable is not set."
fi 
# Tenor
if [[ -v TENOR_API_KEY ]]; then
    echo "Tenor_API_V2_Key=${TENOR_API_KEY}" >> /Rin/Bot/.env
else
    echo "Missing Tenor API key! TENOR_API_KEY environment variable is not set."
fi 
# Top GG
if [[ -v TOP_GG_API_KEY ]]; then
    echo "Top_GG_API_Key=${TOP_GG_API_KEY}" >> /Rin/Bot/.env
else
    echo "Missing Top GG API key! TOP_GG_API_KEY environment variable is not set."
fi
# Twitch access token
if [[ -v TWITCH_API_ACCESS_TOKEN ]]; then
    echo "Twitch_API_Access_Token=${TWITCH_API_ACCESS_TOKEN}" >> /Rin/Bot/.env
else
    echo "Missing Twitch API access token! TWITCH_API_ACCESS_TOKEN environment variable is not set."
fi
# Twitch client ID
if [[ -v TWITCH_API_CLIENT_ID ]]; then
    echo "Twitch_API_Client_ID=${TWITCH_API_CLIENT_ID}" >> /Rin/Bot/.env
else
    echo "Missing Twitch API client id! TWITCH_API_CLIENT_ID environment variable is not set."
fi
# Twitter
if [[ -v TWITTER_BEARER_TOKEN ]]; then
    echo "Twitter_Bearer_Token=${TWITTER_BEARER_TOKEN}" >> /Rin/Bot/.env
else
    echo "Missing Twitter bearer token! TWITTER_BEARER_TOKEN environment variable is not set."
fi
# YouTube
if [[ -v YOUTUBE_API_KEY ]]; then
    echo "YouTube_API_Key=${YOUTUBE_API_KEY}" >> /Rin/Bot/.env
else
    echo "Missing YouTube API key! YOUTUBE_API_KEY environment variable is not set."
fi

exec python3 /Rin/Bot/rinbot.py
