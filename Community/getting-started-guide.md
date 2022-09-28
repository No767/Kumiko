# Getting Started Guide

This guide is meant for end-users who are willing to set up their own version of Kumiko. This allows you to self host your own version of Kumiko, and credits to Ellie (@TheSilkky) for making this all possible.

## Requirements

In order to get started self-hosting your own version of Kumiko, you'll need some of the following installed:

- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)
- [Git](https://git-scm.com/)
- psql and mongosh

If running standalone, you'll also need these:
  - [PostgreSQL](https://www.postgresql.org/)
  - [MongoDB](https://www.mongodb.com/)
  - [Redis](https://redis.io/)
  - [RabbitMQ](https://www.rabbitmq.com/)


> **Note**
> If you are using Docker Desktop, Docker CLI and Docker Compose are already included and installed

## Installation Instructions

Kumiko builds to 2 different Docker Registries: GHCR (GitHub Container Registry) and Docker Hub. You can pull production builds from both, but it is advised to use all production builds from Docker Hub


> **Note**
> Do not use the dev-builds for production. Dev-builds are known to be unstable, and contain breaking changes. And therefore tagged versions or production builds should be used instead


### Docker CLI

1. Pull the latest production build from either GHCR or Docker Hub

    GHCR (Replace `version` with the latest tagged release from GitHub): 
    ```bash
    docker pull ghcr.io/no767/kumiko:version
    ```

    Docker Hub (Replace `version` with the latest tagged release from GitHub and/or from Docker Hub):
    ```bash
    docker pull no767/kumiko:version
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

3. Download the example docker env file. This is the file where you'll put all of your env and credentials in

    curl:

    ```bash
    curl -o .env https://raw.githubusercontent.com/No767/Kumiko/dev/.env-docker-example
    ```

    wget:

    ```bash
    wget -O .env https://raw.githubusercontent.com/No767/Kumiko/dev/.env-docker-example
    ```

4. Add the API keys, access tokens, and database credentials to the `.env` file. Also make sure to get your bot token as well.

5. Now we need to create the databases needed. Log into your Postgres server and create the databases needed (based on the 4 environment variables in the `.env` file that ask for the database names). Also log on to your MongoDB server and create the database needed. The name of the database is `kumiko_marketplace`. 

    So for example, if I had these 4 set like this:

    ```.env
    POSTGRES_ECO_USERS_DB="kumiko_users"
    POSTGRES_WS_DB="kumiko_ws"
    POSTGRES_AH_DB="kumiko_ah"
    POSTGRES_QUESTS_DB="kumiko_quests"
    ```

    then I would have to create the databases like this:

    ```sql
    CREATE DATABASE kumiko_users;
    CREATE DATABASE kumiko_ws;
    CREATE DATABASE kumiko_ah;
    CREATE DATABASE kumiko_quests;
    ```

6. For some parts of Kumiko to work (most notably the Genshin Wish Sim (GWS) system), you'll need to upload some parts of the pre-made data to the PostgreSQL server. To do this, you'll need to run this command to do so:

    ```sh
    psql -U Kumiko -d kumiko_ws < ./WS-Data/ws_data.sql
    ```

    For Dockerized PostgreSQL servers, run this command instead:

    ```sh
    sudo docker exec -i postgres_docker_container psql -U Kumiko -d kumiko_ws < ./WS-Data/ws_data.sql
    ```

7. Once you have everything set, it's finally time to run it. Use this command to run it (replace the image name with the one you pulled from Docker Hub or GHCR):

8. Now it's time to run Kumiko. Just run this command to run the bot:

    ```bash
    sudo docker run -d --restart=always --env-file=.env --name Kumiko no767/kumiko:latest
    ```

> **Note**
> On windows, you don't need to run it with the `sudo` command. 

10. Invite your bot into your server of choice, and have fun!

11. (Optional) Check the logs of the container to make sure that nothing went wrong.
### Docker Compose

1. Download the `.env` file and `docker-compose.yml` file

    curl:
    ```bash
    curl -o .env https://raw.githubusercontent.com/No767/Kumiko/dev/.env-docker-example \
    && curl -o docker-compose.yml https://raw.githubusercontent.com/No767/Kumiko/dev/docker-compose-example.yml
    ```

    wget: 

    ```bash
    wget -O .env https://raw.githubusercontent.com/No767/Kumiko/dev/.env-docker-example \
    && wget -O docker-compose.yml https://raw.githubusercontent.com/No767/Kumiko/dev/docker-compose-example.yml
    ```

    Alternatively, you can also use the `setup.sh` script to help with that.

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

3. Add the API keys, access tokens, and database credentials to the `.env` file. Also make sure to get your bot token as well.

4. Edit the `docker-compose.yml` file to include the credentials of the databases.

5. Now we need to create the databases needed. Log into your Postgres server and create the databases needed (based on the 4 environment variables in the `.env` file that ask for the database names). Also log on to your MongoDB server and create the database needed. The name of the database is `kumiko_marketplace`. 

    So for example, if I had these 4 set like this:

    ```.env
    POSTGRES_ECO_USERS_DB="kumiko_users"
    POSTGRES_WS_DB="kumiko_ws"
    POSTGRES_AH_DB="kumiko_ah"
    POSTGRES_QUESTS_DB="kumiko_quests"
    ```

    then I would have to create the databases like this:

    ```sql
    CREATE DATABASE kumiko_users;
    CREATE DATABASE kumiko_ws;
    CREATE DATABASE kumiko_ah;
    CREATE DATABASE kumiko_quests;
    ```

6. For some parts of Kumiko to work (most notably the Genshin Wish Sim (GWS) system), you'll need to upload some parts of the pre-made data to the PostgreSQL server. To do this, you'll need to run this command to do so:

    ```bash
    psql -U Kumiko -d kumiko_ws < ./WS-Data/ws_data.sql
    ```

    For Dockerized PostgreSQL servers, run this command instead:

    ```bash
    sudo docker exec -i Kumiko-Postgres psql -U Kumiko -d kumiko_ws < ./WS-Data/ws_data.sql

7. Start the Docker Compose stack. Kumiko will automatically create the table when it starts up.

    ```bash
    sudo docker compose up -d
    ```

8. Invite your bot into your server of choice, and have fun!

9. (Optional) Check the logs of the container to make sure that nothing went wrong.

## Getting the Discord Bot

You'll more than likely need to get your discord bot up. So these are the setups to how to do that

![images](../assets/getting-started-assets/create-app.png)

1. Create the app that will be needed for the bot. Once done, you should see the page as shown above

![yesyes](../assets/getting-started-assets/create-bot.png)

2. Now head done to the bot section, and click on the button that says "Add Bot". 

![ewom](../assets/getting-started-assets/allow-bot.png)

3. You'll see a pop-up that asks you if you want to create the bot. 

![intents](../assets/getting-started-assets/allow-intents.png)

4. Make sure to have all 3 of the buttons enabled. Kumiko will need all 3 of them to work.

![whyyy](../assets/getting-started-assets/reset-token.png)

5. You'll see a page just like the one above. We'll need access the the token for the bot, and the only way to do it is to reset the token.

![confirm](../assets/getting-started-assets/allow-reset-token.png)

6. Allow for the token to be reset. Note that if your account is hooked up with 2FA, it will ask you to enter your 2FA code. Go to your authenticator app and enter the code from the app.

![copytoken](../assets/getting-started-assets/copy-token.png)

7. Now click on the copy button and copy the token

8. Put the token in the `.env` file you created.

## Extra Notes

### Expected Uptimes

Discord bots are generally expected to be running 24/7, and are expected to have an uptime of 90-99% when in production. Make sure that the server you are running does not experience issues, or this can cause Kumiko to fail. It is recommended to not stop the bot unless for new updates, or critical downtime issues or server maintenance.

### Cloud Deployment

Kumiko can also be deployed to the cloud. Kumiko will work fine in Azure, GCP, or AWS. In fact, it is recommended to deploy Kumiko to the cloud. Hosts such as PebbleHost will not work here. All you need to do is to pull the image from either GHCR or Docker Hub, and then add the env during setup. Once done, Kumiko can be ran in the cloud.