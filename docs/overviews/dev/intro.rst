Introduction
============

Kumiko is internally built with discord.py. 
This document introduces relevant concepts and instructions for this project.

Prerequisites
-------------

There are some tools that you would need to have installed and prepared before you continue. 
They are listed below:

- `Git <https://git-scm.com>`_
- `Docker <https://docker.com>`_
- `Mise <https://mise.jdx.dev/installing-mise.html>`_ alongside with the environment being `activated <https://mise.jdx.dev/getting-started.html#activate-mise>`_
- Discord Account + App

If you are using Linux, the following dependencies will need to be installed:

.. tab-set::

    .. tab-item:: Debian/Ubuntu

        .. code-block:: bash

            sudo apt-get install libffi-dev libnacl-dev python3-dev libssl-dev

    .. tab-item:: Fedora

        .. code-block:: bash

            sudo dnf install libffi-devel nacl-devel python3-devel openssl-devel

    .. tab-item:: OpenSUSE

        .. code-block:: bash

            sudo zypper in libffi-devel libsodium-devel python3-devel libopenssl-devel

    .. tab-item:: Arch

        .. code-block:: bash

            sudo pacman -S libffi libsodium python3 openssl

.. _database-setup:

Database Setup
--------------

The database used is PostgreSQL By default, a Docker Compose file is included for spinning up these for development. Setup instructions are as follows:

Step 1 - Fork and clone the repository
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Once these tools are installed, fork and clone the repository. This can be done as shown below:

::

    git clone https://github.com/SomeUser/Kumiko


Step 2 - Copy ``.env`` and ``.config.dist.yml`` template
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Copy ``env.dist`` to ``.env``  and ``.config.dist.yml`` to ``config.yml`` and within the root of the repository

.. tab-set::

    .. tab-item:: \*nix and MacOS

        .. code-block:: bash

            cp .env.dist .env && cp .config.dist.yml config.yml

    .. tab-item:: Windows

        .. code-block:: powershell

            copy .env.dist .env
            copy .config.dist.yml config.yml

Step 3 - Modify ``.env`` template
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Open up ``.env`` and modify these entries:

- ``DB_PASSWORD``: Replace the value ``password`` with a random secure password of your choice

Step 4 - Run the Docker Compose stack
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. NOTE::

    On \*nix platforms, ``docker`` must be executed with root privileges through ``sudo``, as the Docker daemon binds to a Unix socket ran by the `root` user. 
    See `Manage Docker as a non-root user <https://docs.docker.com/engine/install/linux-postinstall/#manage-docker-as-a-non-root-user>`_ for further details

Now, all you need to do is to execute this command within the root directory in the repository to spin up the database:

.. tab-set::

    .. tab-item:: \*nix and MacOS

        .. code-block:: bash

            docker compose -f docker/docker-compose.dev.yml --env-file .env up -d

    .. tab-item:: Windows

        .. code-block:: powershell

            docker compose -f docker\docker-compose.dev.yml --env-file .env up -d


To bring it down, run the command as shown below:

.. tab-set::

    .. tab-item:: \*nix and MacOS

        .. code-block:: bash

            docker compose -f docker/docker-compose.dev.yml stop

    .. tab-item:: Windows

        .. code-block:: powershell

            docker compose -f docker\docker-compose.dev.yml stop

.. TIP::

    For convenience, ``mise run bot:docker:up`` and ``mise run bot:docker:stop`` can be utilized instead

Step 5 - Connect to the database
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

In order to verify that our configurations work, we can access the database through a CLI tool such as ``psql``

For example, this is the required URI to utilize for PostgreSQL. Replace ``<password>``` with your configured password:

.. code-block:: bash

    postgresql://postgres:<password>@localhost:5432/kumiko

Development Setup
-----------------

.. important::
  
    You must have PostgreSQL running through Docker before setting up on your local machine. Ensure that you have completed the steps in :ref:`database-setup` before proceeding further

Step 1 - Clone the repository if needed
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Once these tools are installed, fork and clone the repository (if you haven't done so previously). This can be done as shown below:

::

    git clone https://github.com/SomeUser/Kumiko

Step 2 - Copy ``.env`` and ``.config.dist.yml`` template if needed
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Copy ``env.dist`` to ``.env``  and ``.config.dist.yml`` to ``config.yml`` and within the root of the repository (if you haven't done so previously)

.. tab-set::

    .. tab-item:: \*nix and MacOS

        .. code-block:: bash

            cp .env.dist .env && cp .config.dist.yml config.yml

    .. tab-item:: Windows

        .. code-block:: powershell

            copy .env.dist .env
            copy .config.dist.yml config.yml
            

Step 3 - Modify ``.env`` template if needed
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Open up ``.env`` and modify these entries:

- ``DB_PASSWORD``: Replace the value ``password`` with a random secure password of your choice

Step 4 - Modify ``config.yml`` template
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Open up ``config.yml`` and modify these entries:

- ``token``: See `Creating a Bot Account <https://discordpy.readthedocs.io/en/stable/discord.html#creating-a-bot-account>`_ for instructions to obtaining the token. Once completed, paste the token into the ``token`` entry

- ``dev_mode``: Set this to ``true`` to enable development-specific features

- ``postgres_uri``: Replace the value ``<password>`` with a random secure password of your choice


Step 5 - Install development dependencies
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Using `uv <https://docs.astral.sh/uv>`_, install the dependencies as shown below:

::

    uv sync --locked

Alternatively, ``mise run bot:install:dev`` can be used for convenience instead

Step 6 - Apply SQL schema
^^^^^^^^^^^^^^^^^^^^^^^^^

Currently, the database is empty. It doesn't have the schema, or the blueprint on how to store data. Using `Atlas <https://atlasgo.io/>`_, our schema is declared through a master schema (found in ``src/schema.sql``) and  Atlas compares the differences between the current database state and the master schema, and generates and executes a migration plan to get it to the desired state.
But first, apply the schema to the database, which is done as shown below (replace ``<password>`` with your configured PostgreSQL password):

::

    atlas schema apply --auto-approve --env local --var url="postgresql://postgres:<password>@localhost:5432/kumiko?sslmode=disable&search_path=public"

Step 7 - Start the application
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Afterwards, prepare a testing server, invite your development bot, and start the bot to verify that it works.

::

    mise run bot:dev


Details
-------

Development Features
^^^^^^^^^^^^^^^^^^^^

Kumiko includes an development mode allowing for continuous reloading of extensions and utils code. Once the file is saved, the module is reloaded and changes can be reflected. 
This can be enabled through the ``dev_mode`` key in ``config.yml``. In addition, Jishaku is bundled with the bot, allowing for easy debugging and faster development.

.. note::

    You may need to restart the bot entirely for some changes to be reflected.

Prometheus Metrics
^^^^^^^^^^^^^^^^^^

Kumiko also includes an Prometheus endpoint for metrics. This can enabled through the ``prometheus.enabled`` key. If  you don't need this feature, feel free to entirely disable it.
Disabling this feature does not affect the bot, as the cog responsible for this feature is an extension that can be enabled at will.

Type Hinting
^^^^^^^^^^^^

Kumiko actively uses `type hinting <https://docs.python.org/3/library/typing.html>`_ in order to verify for types before runtime.
`Pyright <https://github.com/microsoft/pyright>`_ is used to enforce this standard. Checks happen before you commit, and on Github actions.
These checks are activated by default on VSCode. Pyright is available as a LSP on Neovim.

.. note::

    Future development may use `ty <https://docs.astral.sh/ty/>`_ instead of `Pyright <https://github.com/microsoft/pyright>`_ for better development experience.