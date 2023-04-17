Requirements
==================================


Software Requirements
---------------------
Before you get started, please ensure you have the following installed:

- `Git <https://git-scm.com>`_
- `Python 3 <https://python.org>`_
- `Poetry <https://python-poetry.org>`_
- `WSL2 <https://docs.microsoft.com/en-us/windows/wsl/>`_ (If working on Windows)
- `Docker <https://docker.com>`_
- Discord Account + App

.. NOTE::
    Kumiko is natively developed for Linux. If you are using Windows, please use WSL2. 

Package Prerequisites
----------------------

Debian/Ubuntu
^^^^^^^^^^^^^

.. code-block:: bash

    sudo apt-get install libffi-dev python3-dev libnacl-dev libopus-dev libopus0 \
    libopusenc-dev build-essentials libssl-dev curl wget git

RHEL/CentOS/Fedora 22 or below
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

    sudo yum install make gcc libffi-devel python-devel \
    openssl-devel opus-devel opus curl wget git

Fedora 23+
^^^^^^^^^^

.. code-block:: bash

    sudo dnf install make automake gcc gcc-c++ kernel-devel \
    libffi-devel python3-libnacl python3.11-devel openssl11-devel \
    openssl-devel opus opus-devel curl wget git

OpenSUSE
^^^^^^^^

.. code-block:: bash

    sudo zypper install gcc make automake openssl-devel openssl-1_1 openssl-1_1-devel  \
    libffi-devel python311-devel python311-libnacl opus libopus0 wget git curl

Arch Linux
^^^^^^^^^^

.. code-block:: bash

    sudo pacman -S --needed base-devel openssl openssl-1.1 libffi python python-libnacl opus

MacOS
^^^^^

.. code-block:: bash

    brew install openssl openssl@1.1 libffi git curl make opus