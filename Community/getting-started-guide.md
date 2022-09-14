# Getting Started Guide

This guide is meant for end-users who are willing to set up their own version of Rin. This allows you to self host your own version of Rin, and credits to Ellie (@TheSilkky) for making this all possible.

## Requirements

In order to get started self-hosting your own version of Rin, you'll need some of the following installed:

- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)
- [Git](https://git-scm.com/)

> **Note**
> If you are using Docker Desktop, Docker CLI and Docker Compose are already included and installed

## Installation Instructions

Rin builds to 2 different Docker Registries: GHCR (GitHub Container Registry) and Docker Hub. You can pull production builds from both, but it is advised to use all production builds from Docker Hub


> **Note**
> Do not use the dev-builds for production. Dev-builds are known to be unstable, and contain breaking changes. And therefore tagged versions or production builds should be used instead


### Docker CLI

1. Pull the latest production build from either GHCR or Docker Hub

    GHCR (Replace `version` with the latest tagged release from GitHub): 
    ```sh
    docker pull ghcr.io/no767/rin:latest
    ```

    Docker Hub:
    ```sh
    docker pull no767/rin-prod:latest
    ```
2. Go ahead and get the access tokens and/or API keys for some of the APIs. Here's a list of the services that require API Keys or Access Tokens
    - [Blue Alliance](https://www.thebluealliance.com/apidocs)
    - [Discord.bots.gg](https://discord.bots.gg/) (probably will have to log in first)
    - [FIRST FRC](https://frc-events.firstinspires.org/services/API) 
    - [GitHub](https://docs.github.com/en/rest/guides/basics-of-authentication)
    - [Hypixel](https://api.hypixel.net/#section/Authentication/ApiKey)
    - [Reddit](https://www.reddit.com/prefs/apps) (Get both the ID and Secret)
    - [Tenor](https://developers.google.com/tenor/guides/quickstart#setup)
    - [Top.gg](https://docs.top.gg/)
    - [Twitch](https://dev.twitch.tv/docs/api/get-started) (Get both the Access Token and Client ID. [Use an Implicit grant flow for this](https://dev.twitch.tv/docs/authentication/getting-tokens-oauth#implicit-grant-flow))
    - [Twitter](https://developer.twitter.com/en/docs/twitter-api/getting-started/about-twitter-api) (Get the Bearer Token that supports both API v2 and v1.1)
    - [YouTube](https://developers.google.com/youtube/registering_an_application)

3. Go ahead and get the token for Rin. Save it instead, and this will be used to authorize the bot. Instructions can be found [here](https://github.com/No767/Rin/blob/dev/Community/getting-started-guide.md#getting-the-discord-bot).

4. Download the example docker env file. You'll put your API keys, bot tokens, and access tokens inside there. 

    curl:
    ```sh
    curl -o .env https://raw.githubusercontent.com/No767/Rin/master/.env-docker-example
    ```

    wget: 

    ```sh
    wget -O .env https://raw.githubusercontent.com/No767/Rin/master/.env-docker-example
    ```

5. Invite your bot into your server of choice

6. Adjust the values as needed. Replace `apiKey` with the correct API Keys, ACcess Tokens, Client IDs and Client Secrets. The `TOKEN` env is the token for the bot. Make sure that this is correct, or else the bot will not launch and function. Also make sure to invite your bot to your server first.

> **Note**
> Dev builds require another env var to be set. Set the env var `TESTING_BOT_TOKEN` to the same exact token as the `TOKEN` env var.

7. Now once you have everything set, it's time to run the bot. Use the command below to run the bot

    ```sh
    sudo docker run -d --restart=always --env-file=.env --name=Rin no767/rin-prod:latest
    ```

> **Note**
> If you are using Windows, then you don't need to use `sudo` with the commands.

8. (Optional) Check the logs of the docker container to make sure that you are not missing anything

### Docker Compose

1. Download the `.env-docker-example` file and `docker-compose-example.yml` file

    curl:
    ```sh
    curl -o .env https://raw.githubusercontent.com/No767/Rin/master/.env-docker-example \
    && curl -o docker-compose.yml https://raw.githubusercontent.com/No767/Rin/master/docker-compose-example.yml
    ```

    wget: 

    ```sh
    wget -O .env https://raw.githubusercontent.com/No767/Rin/master/.env-docker-example \
    && wget -O docker-compose.yml https://raw.githubusercontent.com/No767/Rin/master/docker-compose-example.yml
    ```

2. Go ahead and get the access tokens and/or API keys for some of the APIs. Here's a list of the services that require API Keys or Access Tokens
    - [Blue Alliance](https://www.thebluealliance.com/apidocs)
    - [Discord.bots.gg](https://discord.bots.gg/) (probably will have to log in first)
    - [FIRST FRC](https://frc-events.firstinspires.org/services/API) 
    - [GitHub](https://docs.github.com/en/rest/guides/basics-of-authentication)
    - [Hypixel](https://api.hypixel.net/#section/Authentication/ApiKey)
    - [Reddit](https://www.reddit.com/prefs/apps) (Get both the ID and Secret)
    - [Tenor](https://developers.google.com/tenor/guides/quickstart#setup)
    - [Top.gg](https://docs.top.gg/)
    - [Twitch](https://dev.twitch.tv/docs/api/get-started) (Get both the Access Token and Client ID. [Use an Implicit grant flow for this](https://dev.twitch.tv/docs/authentication/getting-tokens-oauth#implicit-grant-flow))
    - [Twitter](https://developer.twitter.com/en/docs/twitter-api/getting-started/about-twitter-api) (Get the Bearer Token that supports both API v2 and v1.1)
    - [YouTube](https://developers.google.com/youtube/registering_an_application)

3. Go ahead and get the token for Rin. Save it instead, and this will be used to authorize the bot. Instructions can be found [here](https://github.com/No767/Rin/blob/dev/Community/getting-started-guide.md#getting-the-discord-bot).

4. Invite your bot into your server of choice

5. Adjust the values as needed (within the `.env` file). Replace `apiKey` with the correct API Keys, ACcess Tokens, Client IDs and Client Secrets. The `TOKEN` env is the token for the bot. Make sure that this is correct, or else the bot will not launch and function. Also make sure to invite your bot to your server first.

> **Note**
> Dev builds require another env var to be set. Set the env var `TESTING_BOT_TOKEN` to the same exact token as the `TOKEN` env var.

6. Now once you have everything set, it's time to run the bot. Use the command below to run the bot

    ```sh
    sudo docker-compose up -d
    ```

    To stop the bot, you can just stop the docker compose stack:

    ```sh
    sudo docker compose stop
    ```

> **Note**
> If you are using Windows, then you don't need to use `sudo` with the commands.

7. (Optional) Check the logs of the docker container to make sure that you are not missing anything


## Getting the Discord Bot

You'll more than likely need to get your discord bot up. So these are the setups to how to do that

![images](../assets/getting-started-assets/create-app.png)

1. Create the app that will be needed for the bot. Once done, you should see the page as shown above

![yesyes](../assets/getting-started-assets/create-bot.png)

2. Now head done to the bot section, and click on the button that says "Add Bot". 

![ewom](../assets/getting-started-assets/allow-bot.png)

3. You'll see a pop-up that asks you if you want to create the bot. 

![intents](../assets/getting-started-assets/allow-intents.png)

4. Make sure to have all 3 of the buttons enabled. Rin will need all 3 of them to work.

![whyyy](../assets/getting-started-assets/reset-token.png)

5. You'll see a page just like the one above. We'll need access the the token for the bot, and the only way to do it is to reset the token.

![confirm](../assets/getting-started-assets/allow-reset-token.png)

6. Allow for the token to be reset. Note that if your account is hooked up with 2FA, it will ask you to enter your 2FA code. Go to your authenticator app and enter the code from the app.

![copytoken](../assets/getting-started-assets/copy-token.png)

7. Now click on the copy button and copy the token

8. Now head back the to the docker run command, and switch out the env vars as needed (replace `...` with your discord bot token):

  ```sh
  TOKEN=...
  ```

  > **Note**
  > On dev builds, also add the `TESTING_BOT_TOKEN` env var and use the same exact token for that instead. It'll read it off of that instead

## Extra Notes

### Expected Uptimes

Discord bots are generally expected to be running 24/7, and are expected to have an uptime of 90-99% when in production. Make sure that the server you are running does not experience issues, or this can cause Rin to fail. It is recommended to not stop the bot unless for new updates, or critical downtime issues or server maintenance.

### Cloud Deployment

Rin can also be deployed to the cloud. Rin will work fine in Azure, GCP, or AWS. In fact, it is recommended to deploy Rin to the cloud. Hosts such as PebbleHost will not work here. All you need to do is to pull the image from either GHCR or Docker Hub, and then add the env during setup. Once done, Rin can be ran in the cloud. And also fun fact: Rin v1 was originally deployed to Azure before I started to self-host Rin.
