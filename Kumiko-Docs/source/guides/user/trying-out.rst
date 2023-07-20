Trying out Kumiko
==================

Kumiko can be tried out by running the Docker image. For the official versions of Kumiko, please invite the bot into your guild instead. For those who want to try out the latest breaking features, using Docker is recommended.

Prerequisites
-------------

1. Make sure you have set up your bot token. Refer to :doc:`bot-setup` for the full guide.
2. Make sure you have these installed:
    - `Docker <https://www.docker.com/>`_
    - curl or wget
    - Git

Standalone Prerequisites
^^^^^^^^^^^^^^^^^^^^^^^^

If you are running Kumiko on a standalone machine (w/o Docker Compose or using Systemd), you will need to install the following:

- `PostgreSQL <https://www.postgresql.org/>`_ (w/ ``pg_trgm`` extension loaded)
- `Redis Stack <https://redis.io/docs/stack>`_ (or Redis w/ RedisJSON and RedisSearch modules loaded)


Docker CLI (Standalone)
-----------------------

1. Pull the image from either GHCR or Docker Hub
    
        - GHCR
    
            .. code-block:: bash
    
                docker pull ghcr.io/no767/kumiko:latest
    
        - Docker Hub
    
            .. code-block:: bash
    
                docker pull no767/kumiko:latest

2. Set up the docker ENV file

        .. code-block:: bash
    
            curl -o https://raw.githubusercontent.com/no767/kumiko/master/Envs/docker.env .env

            # Or using wget:

            wget -O .env https://raw.githubusercontent.com/no767/kumiko/master/Envs/docker.env

3. Edit the ``.env`` file to include any credentials needed for the bot to run
    
    .. code-block:: bash
        
        # THIS IS ONLY AN EXAMPLE
        POSTGRES_PASSWORD=...
        POSTGRES_USER=...
        POSTGRES_URI=postgres://user:somepass@localhost:5432/somedb

4. Run the bot

    .. code-block:: bash

        docker run -d --env-file=.env --name Kumiko no767/kumiko:latest

Systemd (Standalone)
--------------------

**Before you start, ensure that you have PostgreSQL and Redis correctly configured and is running**

1. Ensure that the database is created and the PostgreSQL extension ``pg_trgm`` and the RedisJSON module are loaded. Refer to the `Redis docs <https://redis.io/docs/data-types/json/#download-binaries>`_ on how to install and load the JSON module.

    .. code-block:: sql
        
        CREATE ROLE kumiko WITH LOGIN PASSWORD 'somepass';
        CREATE DATABASE kumiko OWNER kumiko;
        CREATE EXTENSION IF NOT EXISTS pg_trgm;

2. Clone the repo

    .. code-block:: bash

        git clone https://github.com/No767/Kumiko.git && cd Kumiko
    

    Or if you have the ``gh`` cli tool installed:

    .. code-block:: bash

        gh repo clone No767/Kumiko

    .. note:: 

        By default, this will clone the dev branch. For stable releases, run ``git checkout master`` to checkout into stable releases (or checkout the latest tag)

3. Set up the prod ENV file. During this step, please also fill your credentials in the ENV file 

    .. code-block:: bash
        
        cp Envs/prod.env Bot/.env

4. Create an venv so that you can install the dependencies without polluting your system

    .. code-block:: bash

        python3 -m venv ./venv

5. Activate the venv, install the dependencies, and then deactivate it

    .. code-block:: bash

        source ./venv/bin/activate \
        && pip install -r Requirements/prod.txt \
        && deactivate

6. Create an systemd service file. This is an example, and you will need to edit it to point to the correct directory and user.

    .. code-block:: ini

        [Unit]
        Description=Kumiko
        After=network-online.target
        Requires=postgresql.service

        [Service]
        Type=simple
        WorkingDirectory=/your/bots/directory
        ExecStart=/your/bots/directory/venv/bin/python3 /your/bots/directory/Bot/kumikobot.py
        User=username
        Restart=on-failure
        EnvironmentFile=/your/bots/directory/Bot/.env

        [Install]
        WantedBy=multi-user.target

7. Test whether you have everything set up. If you have ``make`` installed, you can run ``make prod-run`` in order to run the bot (the ``Makefile`` is found in the root of the repo). Otherwise, just run ``kumikobot.py``

8. Reload the system daemon

    .. code-block:: bash

        sudo systemctl daemon-reload

9. Run and enable the systemd service. 
    
    .. code-block:: bash

        sudo systemctl enable --now kumiko

Docker Compose
--------------

1. Clone the repo

    .. code-block:: bash

        git clone https://github.com/No767/Kumiko.git && cd Kumiko
    

    Or if you have the ``gh`` cli tool installed:

    .. code-block:: bash

        gh repo clone No767/Kumiko

    .. note:: 

        By default, this will clone the dev branch. For stable releases, run ``git checkout master`` to checkout into stable releases (or checkout the latest tag)

2. Copy the ENV files into the correct places

    .. code-block:: bash

        cp Envs/docker.env .env

3. Edit the ``.env`` file placed in the root of the repo to include any credentials needed for the bot to run
    
    .. code-block:: bash
        
        # THIS IS ONLY AN EXAMPLE
        POSTGRES_PASSWORD=...
        POSTGRES_USER=...
        POSTGRES_URI=postgres://user:somepass@localhost:5432/somedb

4. Once everything is set, literally just fire up the whole entire Docker Compose stack. All of the database creation, and the migrations will be done automatically.

    .. code-block:: bash

        docker-compose up -d
