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

If you are running Kumiko on a standalone machine (w/o Docker Compose or using Systemd), you will need to install the following:

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

Standalone (Systemd)
--------------------

**Before you start, ensure that you have PostgreSQL and Redis correctly configured and is running**

1. Clone the repo

    .. code-block:: bash

        git clone https://github.com/No767/Kumiko.git && cd Kumiko
    

    Or if you have the `gh` cli tool installed:

    .. code-block:: bash

        gh repo clone No767/Kumiko

    .. note:: 

        By default, this will clone the dev branch. For stable releases, run ``git checkout master`` to checkout into stable releases (or checkout the latest tag)

2. Set up the prod ENV file. During this step, please also fill your credentials in the ENV file 

    .. code-block:: bash
        
        cp Envs/prod.env Bot/.env

2. Create an systemd service file. This is an example, and you will need to edit it to point to the correct directory and user.

    .. code-block:: ini

        [Unit]
        Description=Kumiko
        After=network-online.target
        Requires=postgresql.service

        [Service]
        Type=simple
        WorkingDirectory=/your/bots/directory
        ExecStart=/usr/bin/python3 /your/bots/directory/Bot/kumikobot.py
        User=username
        Restart=on-failure
        EnvironmentFile=/your/bots/directory/Bot/.env

        [Install]
        WantedBy=multi-user.target

3. Test whether you have everything set up. If you have ``make`` installed, you can run ``make prod-run`` in order to run the bot. Otherwise, just run ``kumikobot.py``

4. Run and enable the systemd service. 
    
    .. code-block:: bash

        sudo systemctl enable --now kumiko

Docker Compose
--------------

1. Download the `.env` file and `docker-compose.yml` file via the `setup.sh` script

    .. code-block:: bash

        curl -s https://raw.githubusercontent.com/No767/Kumiko/master/scripts/setup.sh | sh

2. Obtain the API keys, access tokens, discord bot token, and database credentials for Kumiko. Open up the ``.env`` file with an editor like Vim and add the needed values.

3. Once everything is set, literally just fire up the whole entire Docker Compose stack. All of the database creation, and the seeding of the data will be handled automatically

    .. code-block:: bash

        sudo docker-compose up -d


