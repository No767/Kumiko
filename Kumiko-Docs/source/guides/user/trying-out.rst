Trying out Kumiko
==================

Kumiko can be tried out by running the Docker image. For the official versions of Kumiko, please invite the bot into your guild instead. For those who want to try out the latest breaking features, using Docker is recommended.

Prerequisites
-------------

1. Make sure you have set up your bot token. Refer to :doc:`bot-setup` for the full guide.
2. Make sure you have these installed:
    - `Docker <https://www.docker.com/>`_
    - curl or wget

Standalone Requirements
^^^^^^^^^^^^^^^^^^^^^^^

If you are running Kumiko on a standalone machine (w/o Docker Compose), you will need to install the following:

- `PostgreSQL <https://www.postgresql.org/>`_
- `Redis Stack <https://redis.io/docs/stack>`_ (or Redis w/ RedisJSON and RedisSearch modules loaded)

Standalone (Docker CLI)
-----------------------

1. Pull the image from either GHCR or Docker Hub
    
        - GHCR
    
            .. code-block:: bash
    
                docker pull ghcr.io/no767/kumiko:latest
    
        - Docker Hub
    
            .. code-block:: bash
    
                docker pull no767/kumiko:latest

2. Download the example docker env file and standalone-setup script. This is the file where you'll put all of your env and credentials in

        .. code-block:: bash
    
            curl -o https://raw.githubusercontent.com/no767/kumiko/master/.env-docker-example .env

            # Or using wget:

            wget -O .env https://raw.githubusercontent.com/no767/kumiko/master/.env-docker-example 

3. Obtain the API keys, access tokens, discord bot token, and database credentials for Kumiko. Open up the ``.env`` file with an editor like Vim and add the needed values.

4. Now it's time to run Kumiko. Just run this command to run the bot:

        .. code-block:: bash
    
            sudo docker run -d --env-file .env --name Kumiko no767/kumiko:latest

Docker Compose
--------------

1. Download the `.env` file and `docker-compose.yml` file via the `setup.sh` script

    .. code-block:: bash

        curl -s https://raw.githubusercontent.com/No767/Kumiko/master/scripts/setup.sh | sh

2. Obtain the API keys, access tokens, discord bot token, and database credentials for Kumiko. Open up the ``.env`` file with an editor like Vim and add the needed values.

3. Once everything is set, literally just fire up the whole entire Docker Compose stack. All of the database creation, and the seeding of the data will be handled automatically

    .. code-block:: bash

        sudo docker-compose up -d


