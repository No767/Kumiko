# Getting Started Guide

This guide is meant for end-users who are willing to set up their own version of Kumiko. This allows you to self host your own version of Kumiko, and credits to Ellie (@TheSilkky) for making this all possible.

## Requirements

In order to get started self-hosting your own version of Kumiko, you'll need some of the following installed:

- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)
- [Poetry](https://python-poetry.org/)
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
    ```sh
    docker pull ghcr.io/no767/kumiko:version
    ```

    Docker Hub (Replace `version` with the latest tagged release from GitHub and/or from Docker Hub):
    ```sh
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

3. Clone the GitHub repo and `cd` int to the directory

    ```sh
    git clone https://github.com/No767/Kumiko.git && cd Kumiko
    ```

4. Rename the `.env-docker-example` file to `.env`

5. Add the API keys, access tokens, and database credentials to the `.env` file. Also make sure to get your bot token as well.

6. Now we need to create the databases needed. Log into your Postgres server and create the databases needed (based on the 4 environment variables in the `.env` file that ask for the database names). Also log on to your MongoDB server and create the database needed. The name of the database is `kumiko_marketplace`. 

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

7. For some parts of Kumiko to work (most notably the Genshin Wish Sim (GWS) system), you'll need to upload some parts of the pre-made data to the PostgreSQL server. To do this, you'll need to run this command to do so:

    ```sh
    psql -U Kumiko -d kumiko_ws < ./WS-Data/ws_data.sql
    ```

    For Dockerized PostgreSQL servers, run this command instead:

    ```sh
    sudo docker exec -i postgres_docker_container psql -U Kumiko -d kumiko_ws < ./WS-Data/ws_data.sql
    ```

8. Now it's time to seed the databases. Create and set up a poetry env, and run the `postgres-init.py` file located in the `scripts` directory. This will basically create the tables needed. Later on, Kumiko will have an automatic system for dealing with this.

    ```sh
    poetry env use 3.10
    poetry install
    poetry run python scripts/postgres-init.py
    ```

9. Once you have everything set, it's finally time to run it. Use this command to run it (replace the image name with the one you pulled from Docker Hub or GHCR):

4. Download the example docker env file. You'll put your API keys, bot tokens, and access tokens inside there. 

    ```sh
    sudo docker run -d --restart=always --env-file=.env --name Kumiko no767/kumiko:version
    ```

> **Note**
> On windows, you don't need to run it with the `sudo` command. 

10. Invite your bot into your server of choice, and have fun!

11. (Optional) Check the logs of the container to make sure that nothing went wrong.
### Docker Compose

1. Download the `.env-docker-example` file and `docker-compose-example.yml` file

```sh
git clone https://github.com/No767/Kumiko
```

2. Find the `docker-compose-example.yml` file and rename it to `docker-compose.yml` And also rename the `.env-docker-example` file to `.env`.

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

4. Add the API keys, access tokens, and database credentials to the `.env` file. Also make sure to get your bot token as well.

5. Edit the `docker-compose.yml` file to include the credentials of the databases.

6. Notice that the section where Kumiko would normally be started up is commented out. Leave it like so for now, we'll get back to it. Start the Docker Compose stack.

    ```sh
    sudo docker compose up -d
    ```

7. Now we need to create the databases needed. Log into your Postgres server and create the databases needed (based on the 4 environment variables in the `.env` file that ask for the database names). Also log on to your MongoDB server and create the database needed. The name of the database is `kumiko_marketplace`. 

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

8. Now it's time to seed the databases. Create and set up a poetry env, and run the `postgres-init.py` file located in the `scripts` directory. This will basically create the tables needed. Later on, Kumiko will have an automatic system for dealing with this.

    ```sh
    poetry env use 3.10
    poetry install
    poetry run python scripts/postgres-init.py
    ```


9. For some parts of Kumiko to work (most notably the Genshin Wish Sim (GWS) system), you'll need to upload some parts of the pre-made data to the PostgreSQL server. To do this, you'll need to run this command to do so:

    ```sh
    psql -U Kumiko -d kumiko_ws < ./WS-Data/ws_data.sql
    ```

    For Dockerized PostgreSQL servers, run this command instead:

    ```sh
    sudo docker exec -i Kumiko-Postgres psql -U Kumiko -d kumiko_ws < ./WS-Data/ws_data.sql
    ```
10. Now stop the Docker Compose stack. Comment out the part where Kumiko should start. Since you have all of the databases and tables set up, Kumiko should hopefully work properly now.

    ```sh
    sudo docker compose stop
    ```

    If you noticed beforehand, the Docker Compose file had this section commented out:

    ```yaml
    services:
      # kumiko:
      #   container_name: Kumiko
      #   image: no767/kumiko:version # Replace version with the latest tagged version from Docker Hub
      #   restart: always
      #   deploy:
      #     restart_policy:
      #       condition: on-failure
      #       delay: 0s
      #       max_attempts: 3
      #       window: 120s
      #     mode: replicated
      #   env_file:
      #     - .env
    ```

    Now it should look like this:
    ```yaml
    services:
      kumiko:
      container_name: Kumiko
      image: no767/kumiko:version # Replace version with the latest tagged version from Docker Hub
      restart: always
      deploy:
        restart_policy:
          condition: on-failure
          delay: 0s
          max_attempts: 3
          window: 120s
        mode: replicated
      env_file:
        - .env
    ```

11. Start the Docker Compose stack again. This time, Kumiko is included, and hopefully should run along with all of the other docker containers as well.

    ```sh
    sudo docker compose up -d
    ```

12. Invite your bot into your server of choice, and have fun!

13. (Optional) Check the logs of the container to make sure that nothing went wrong.

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