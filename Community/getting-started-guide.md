# Getting Started Guide

This guide is meant for end-users who are willing to set up their own version of Rin. This allows you to self host your own version of Rin, and credits to Ellie (@TheSilkky) for making this all possible.

## Requirements

In order to get started self-hosting your own version of Rin, you'll need some of the following installed:

- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)
- [Git](https://git-scm.com/)

> NOTE: If you are using Docker Desktop, Docker CLI and Docker Compose are already included and installed

## Installation Instructions

Rin builds to 2 different Docker Registries: GHCR (GitHub Container Registry) and Docker Hub. You can pull production builds from both, but it is advised to use all production builds from Docker Hub

> NOTE: Do not use the dev-builds for production. Dev-builds are known to be unstable, and contain breaking changes. And therefore tagged versions or production builds should be used instead

### Docker CLI

1. Pull the latest production build from either GHCR or Docker Hub

    GHCR (Replace `version` with the latest tagged release from GitHub): 
    ```sh
    docker pull ghcr.io/no767/rin:version
    ```

    Docker Hub:
    ```sh
    docker pull no767/rin-prod:latest
    ```
2. Go ahead and get the access tokens and/or API keys for some of the APIs. Here's a list of the services that require API Keys or Access Tokens
    - [Blue Alliance](https://www.thebluealliance.com/apidocs)
    - Discord.bots.gg
    - [FIRST FRC](https://frc-events.firstinspires.org/services/API) 
    - [GitHub](https://docs.github.com/en/rest/guides/basics-of-authentication)
    - [Hypixel](https://api.hypixel.net/#section/Authentication/ApiKey)
    - [Reddit](https://www.reddit.com/prefs/apps) (Get both the ID and Secret)
    - [Tenor](https://developers.google.com/tenor/guides/quickstart#setup)
    - [Top.gg](https://docs.top.gg/)
    - [Twitch](https://dev.twitch.tv/docs/api/get-started) (Get both the Access Token and Client ID. [Use an Implicit grant flow for this](https://dev.twitch.tv/docs/authentication/getting-tokens-oauth#implicit-grant-flow))
    - [Twitter](https://developer.twitter.com/en/docs/twitter-api/getting-started/about-twitter-api) (Get the Bearer Token that supports both API v2 and v1.1)
    - [YouTube](https://developers.google.com/youtube/registering_an_application)

3. Go ahead and get the token for Rin. Save it instead, and this will be used to authorize the bot. Instructions can be found [here](https://github.com/No767/Rin/blob/dev/Community/getting-started-rin.md#getting-the-discord-bot).


4. Invite your bot into your server of choice

5. Now once you have all of the API keys and Access Tokens, now you can use the `-e` flag to add it in. 

```sh
sudo docker run -d \
-e TOKEN=botToken \
-e BLUE_ALLIANCE_API_KEY=apiKey \
-e DISCORD_BOTS_API_KEY=apiKey \
-e FIRST_EVENTS_FINAL_KEY=apiKey \
-e GITHUB_API_ACCESS_TOKEN=apiKey \
-e HYPIXEL_API_KEY=apiKey \
-e REDDIT_ID=apiKey \
-e REDDIT_SECRET=apiKey \
-e TENOR_API_KEY=apiKey \
-e TOP_GG_API_KEY=apiKey \
-e TWITCH_API_ACCESS_TOKEN=apiKey \
-e TWITCH_API_CLIENT_ID=apiKey \
-e TWITTER_BEARER_TOKEN=apiKey \
-e YOUTUBE_API_KEY=apiKey \
--restart=always \
--name Rin \
no767/rin-prod:latest
```

Replace `apiKey` with the correct API Keys, Access Tokens, Client IDs and Client Secrets. The `TOKEN` env is the token for the bot. Make sure that this is correct, or else the bot will not launch and function. Also make sure to invite your bot to your server first.

6. Run the docker container, and check the logs to make sure that you are not missing anything

### Docker Compose

1. Clone the repo

```sh
git clone https://github.com/No767/Rin
```

2. Find the `docker-compose-example.yml` file and rename it to `docker-compose.yml`

3. Go ahead and get the access tokens and/or API keys for some of the APIs. Here's a list of the services that require API Keys or Access Tokens
    - [Blue Alliance](https://www.thebluealliance.com/apidocs)
    - Discord.bots.gg
    - [FIRST FRC](https://frc-events.firstinspires.org/services/API) 
    - [GitHub](https://docs.github.com/en/rest/guides/basics-of-authentication)
    - [Hypixel](https://api.hypixel.net/#section/Authentication/ApiKey)
    - [Reddit](https://www.reddit.com/prefs/apps) (Get both the ID and Secret)
    - [Tenor](https://developers.google.com/tenor/guides/quickstart#setup)
    - [Top.gg](https://docs.top.gg/)
    - [Twitch](https://dev.twitch.tv/docs/api/get-started) (Get both the Access Token and Client ID. [Use an Implicit grant flow for this](https://dev.twitch.tv/docs/authentication/getting-tokens-oauth#implicit-grant-flow))
    - [Twitter](https://developer.twitter.com/en/docs/twitter-api/getting-started/about-twitter-api) (Get the Bearer Token that supports both API v2 and v1.1)
    - [YouTube](https://developers.google.com/youtube/registering_an_application)

4. Go ahead and get the token for Rin. Save it instead, and this will be used to authorize the bot. Instructions can be found [here](https://github.com/No767/Rin/blob/dev/Community/getting-started-rin.md#getting-the-discord-bot).

5. Invite your bot into your server of choice

6. Now add the correct values into the docker compose file. A reference for the Docker Compose file is provided below:

```yaml
# docker-compose-example.yml
version: "3.9"
services:
  rin:
    # Use cloudflare's DNS server. This is what Discord uses as well
    # May have issues...
    dns: 
      - 1.1.1.1
      - 1.0.0.1
    container_name: Rin
    restart: always
    image: no767/rin-prod:latest
    deploy:
      restart_policy:
        condition: on-failure
        delay: 0s
        max_attempts: 3
        window: 120s
      mode: replicated
    environment:
      # Replace these values with the correct values
      - TOKEN=botToken 
      - BLUE_ALLIANCE_API_KEY=apiKey 
      - DISCORD_BOTS_API_KEY=apiKey 
      - FIRST_EVENTS_FINAL_KEY=apiKey 
      - GITHUB_API_ACCESS_TOKEN=apiKey 
      - HYPIXEL_API_KEY=apiKey 
      - REDDIT_ID=apiKey 
      - REDDIT_SECRET=apiKey 
      - TENOR_API_KEY=apiKey 
      - TOP_GG_API_KEY=apiKey 
      - TWITCH_API_ACCESS_TOKEN=apiKey 
      - TWITCH_API_CLIENT_ID=apiKey 
      - TWITTER_BEARER_TOKEN=apiKey 
      - YOUTUBE_API_KEY=apiKey 
```

7. Run `sudo docker compose up -d` to fire up the docker compose project, and Rin should be running. Use `sudo docker compose stop` to stop Rin as needed. 

## Extra Notes

### Expected Uptimes

Discord bots are generally expected to be running 24/7, and are expected to have an uptime of 90-99% when in production. Make sure that the server you are running does not experience issues, or this can cause Rin to fail. It is recommended to not stop the bot unless for new updates, or critical downtime issues or server maintenance.

### Cloud Deployment

Rin can also be deployed to the cloud. Rin will work fine in Azure, GCP, or AWS. In fact, it is recommended to deploy Rin to the cloud. Hosts such as PebbleHost will not work here. All you need to do is to pull the image from either GHCR or Docker Hub, and then add the env during setup. Once done, Rin can be ran in the cloud. And also fun fact: Rin v1 was originally deployed to Azure before I started to self-host Rin.