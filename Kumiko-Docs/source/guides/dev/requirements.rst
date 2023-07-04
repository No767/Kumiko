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

    sudo apt-get install libffi-dev python3-dev libnacl-dev libopus-dev  \
    libopusenc-dev build-essentials libssl-dev curl wget git


Fedora
^^^^^^^^^^

.. code-block:: bash

    sudo dnf install make automake gcc gcc-c++ kernel-devel \
    libffi-devel python3-libnacl python3.11-devel openssl-devel \
    opus-devel curl wget git

OpenSUSE
^^^^^^^^

.. code-block:: bash

    sudo zypper install gcc make automake openssl-devel libffi-devel \
    python311-devel python311-libnacl libopus0 wget git curl

Arch Linux
^^^^^^^^^^

.. code-block:: bash

    sudo pacman -S --needed base-devel openssl libffi python python-libnacl opus

MacOS
^^^^^

.. code-block:: bash

    brew install openssl libffi git curl make opus
