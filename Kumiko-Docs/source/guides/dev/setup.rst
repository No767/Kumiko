Setup
========

Local Setup
-----------

1. Fork and clone the repo

    .. code-block:: bash

        git clone https://github.com/[username]/Kumiko.git && cd Kumiko
    

    Or if you have the `gh` cli tool installed:

    .. code-block:: bash

        gh repo clone [username]/Kumiko
    

2. Install all of the dependencies (including dev dependencies)

    .. code-block:: bash

        poetry install --with=dev,test,docs

3. Copy the ENV files into the correct places

    .. code-block:: bash

        cp Envs/dev.env Bot/.env \
        cp Envs/docker.env .env

4. Edit the ``.env`` file placed in the root of the repo and in the ``Bot`` folder to include any credentials needed for the bot to run
    
    .. code-block:: bash
        
        # THIS IS ONLY AN EXAMPLE
        POSTGRES_PASSWORD=...
        POSTGRES_USER=...
        POSTGRES_URI=postgres://user:somepass@localhost:5432/somedb
        

5. Start the Docker Compose stack

    .. code-block:: bash

        sudo docker compose -f docker-compose-dev.yml up -d
    

6. Enable the PostgreSQL extension ``pg_trgm``

    .. code-block:: sql

        CREATE EXTENSION pg_trgm;

7. Run the database migrations

    .. code-block:: bash

        python migrations-runner.py
    
Vagrant
-------

Kumiko also supports using Vagrant as a development environment. 

.. note::

    The Ansible playbook only sets up the environment which includes everything needed to get started. There is still a layer of manual configuration that needs to be done. The Ansible playbook installs PostgreSQL, Redis, Python and Poetry into the VM, and also sets up the repo for development. There is no need to use Docker since PostgreSQL and Redis are installed natively into the system.

Requirements
^^^^^^^^^^^^

* Vagrant (w/ `VirtualBox WSL2 plugin <https://github.com/Karandash8/virtualbox_WSL2>`_)
* WSL2
* Ansible (installed on WSL2 (you will need to execute the vagrant commands in WSL2))

Ansible roles needed:

* ``geerlingguy.postgresql``
* ``geerlingguy.redis``
* ``staticdev.pyenv``


In order to use Vagrant, you will need Oracle VirtualBox or VMWare Workstation installed on your machine. Once installed and properly configured, you can just run ``vagrant up`` (in your WSL2 or Linux environment) to provision and start it up, and connect to it by SSH or by VSCode. 

Environment Variables
---------------------

Kumiko v0.7+ includes an development mode feature, which will set up jishaku and a custom FS watcher. The FS (File System) watcher is just like HMR (Hot Module Replacements). Once you press Ctrl+s in your cog, it will automatically reload it so the code executed is changed. Later on, there may be more development features that will be included. Make sure you first install the dev dependencies first! And in order to enable it, set an environment variable called ``DEV_MODE`` to ``True``.