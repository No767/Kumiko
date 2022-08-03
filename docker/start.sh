#!/usr/bin/env bash

# Note that this won't be used on Kumiko. Kumiko uses a different system instead

set -euo pipefail

if [[ -v TOKEN ]]; then
    sed -i "s@bot_token@$TOKEN@g" /Rin/Bot/.env
else
    echo "Missing bot token! TOKEN environment variable is not set."
    exit 1;
fi 


# API Keys
# Blue Alliance
if [[ -v BLUE_ALLIANCE_API_KEY ]]; then
    sed -i "s@blue_alliance_api_key@$BLUE_ALLIANCE_API_KEY@g" /Rin/Bot/.env
else
    echo "Missing Blue Alliance API key! BLUE_ALLIANCE_API_KEY environment variable is not set."
    exit 1;
fi 
# Discord
if [[ -v DISCORD_BOTS_API_KEY ]]; then
    sed -i "s@discord_bots_api_key@$DISCORD_BOTS_API_KEY@g" /Rin/Bot/.env
else
    echo "Missing Discord Bots API key! DISCORD_BOTS_API_KEY environment variable is not set."
    exit 1;
fi 
# First Events
if [[ -v FIRST_EVENTS_FINAL_KEY ]]; then
    sed -i "s@first_events_final_key@$FIRST_EVENTS_FINAL_KEY@g" /Rin/Bot/.env
else
    echo "Missing First Events Final key! FIRST_EVENTS_FINAL_KEY environment variable is not set."
    exit 1;
fi 
# GitHub
if [[ -v GITHUB_API_ACCESS_TOKEN ]]; then
    sed -i "s@github_api_access_token@$GITHUB_API_ACCESS_TOKEN@g" /Rin/Bot/.env
else
    echo "Missing GitHub API token! GITHUB_API_ACCESS_TOKEN environment variable is not set."
    exit 1;
fi 
# Hypixel
if [[ -v HYPIXEL_API_KEY ]]; then
    sed -i "s@hypixel_api_key@$HYPIXEL_API_KEY@g" /Rin/Bot/.env
else
    echo "Missing Hypixel API key! HYPIXEL_API_KEY environment variable is not set."
    exit 1;
fi 
# Reddit ID
if [[ -v REDDIT_ID ]]; then
    sed -i "s@reddit_id@$REDDIT_ID@g" /Rin/Bot/.env
else
    echo "Missing Reddit ID! REDDIT_ID environment variable is not set."
    exit 1;
fi 
# Reddit Secret
if [[ -v REDDIT_SECRET ]]; then
    sed -i "s@reddit_secret@$REDDIT_SECRET@g" /Rin/Bot/.env
else
    echo "Missing Reddit secret! REDDIT_SECRET environment variable is not set."
    exit 1;
fi 
# Tenor
if [[ -v TENOR_API_KEY ]]; then
    sed -i "s@tenor_api_key@$TENOR_API_KEY@g" /Rin/Bot/.env
else
    echo "Missing Tenor API key! TENOR_API_KEY environment variable is not set."
    exit 1;
fi 
# Top GG
if [[ -v TOP_GG_API_KEY ]]; then
    sed -i "s@top_gg_api_key@$TOP_GG_API_KEY@g" /Rin/Bot/.env
else
    echo "Missing Top GG API key! TOP_GG_API_KEY environment variable is not set."
    exit 1;
fi
# Twitch access token
if [[ -v TWITCH_API_ACCESS_TOKEN ]]; then
    sed -i "s@twitch_api_access_token@$TWITCH_API_ACCESS_TOKEN@g" /Rin/Bot/.env
else
    echo "Missing Twitch API access token! TWITCH_API_ACCESS_TOKEN environment variable is not set."
    exit 1;
fi
# Twitch client ID
if [[ -v TWITCH_API_CLIENT_ID ]]; then
    sed -i "s@twitch_api_client_id@$TWITCH_API_CLIENT_ID@g" /Rin/Bot/.env
else
    echo "Missing Twitch API client id! TWITCH_API_CLIENT_ID environment variable is not set."
    exit 1;
fi
# Twitter
if [[ -v TWITTER_BEARER_TOKEN ]]; then
    sed -i "s@twitter_bearer_token@$TWITTER_BEARER_TOKEN@g" /Rin/Bot/.env
else
    echo "Missing Twitter bearer token! TWITTER_BEARER_TOKEN environment variable is not set."
    exit 1;
fi
# YouTube
if [[ -v YOUTUBE_API_KEY ]]; then
    sed -i "s@youtube_api_key@$YOUTUBE_API_KEY@g" /Rin/Bot/.env
else
    echo "Missing YouTube API key! YOUTUBE_API_KEY environment variable is not set."
    exit 1;
fi

exec python3 /Rin/Bot/rinbot.py
