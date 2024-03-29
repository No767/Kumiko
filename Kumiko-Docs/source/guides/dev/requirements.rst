Requirements
==================================


Software Requirements
---------------------
Before you get started, please ensure you have the following installed:

- `Git <https://git-scm.com>`_
- `Python 3 <https://python.org>`_
- `Poetry <https://python-poetry.org>`_
- `Docker <https://docker.com>`_
- Discord Account + App

.. CAUTION::
   Kumiko is natively developed for Linux. 
   Development should work on Windows but it is highly untested.

Package Prerequisites
----------------------

Debian/Ubuntu
^^^^^^^^^^^^^

.. code-block:: bash

    sudo apt-get install libffi-dev python3-dev \
    libnacl-dev libssl-dev curl wget git make


Fedora
^^^^^^^^^^

.. code-block:: bash

    sudo dnf install make libffi-devel python3-libnacl \
    python3.11-devel openssl-devel curl wget git

OpenSUSE
^^^^^^^^

.. code-block:: bash

    sudo zypper install make openssl-devel libffi-devel \
    python311-devel python311-libnacl wget git curl

Arch Linux
^^^^^^^^^^

.. code-block:: bash

    sudo pacman -S --needed base-devel openssl libffi python python-libnacl

MacOS
^^^^^

.. code-block:: bash

    brew install openssl libffi git curl make
