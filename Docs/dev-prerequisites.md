# Dev Prerequisites

## Software Prerequisites

Before you get started, please ensure you have the following installed:

- [Git](https://git-scm.com/)
- [Python 3](https://www.python.org/) (Python 3.11 is what the codebase uses)
- [Poetry](https://python-poetry.org/)
- [Pyenv](https://github.com/pyenv/pyenv) (Optional, Recommended)
- [WSL2](https://docs.microsoft.com/en-us/windows/wsl/) (If working on Windows)
- [Docker](https://www.docker.com/) (Use [Docker Engine](https://docs.docker.com/engine/) on Linux, [Docker Desktop](https://www.docker.com/products/docker-desktop/) on Windows/WSL2, MacOS and Linux (beta))
- Discord Account + Discord App

> **Note**
> Kumiko is natively developed for Linux. If you are using Windows, please use WSL2. 

## Package Prerequisites

### Debian/Ubuntu

```sh 
sudo apt-get install libffi-dev python3-dev libnacl-dev libopus-dev libopus0 libopusenc-dev build-essentials \
libssl-dev curl wget git
```

### RHEL/CentOS/Fedora 22 or below

```sh
sudo yum install make gcc libffi-devel python-devel \
openssl-devel opus-devel opus curl wget git
```

### Fedora 23+

```sh
sudo dnf install make automake gcc gcc-c++ kernel-devel \
libffi-devel python3-libnacl python3.11-devel openssl11-devel \
openssl-devel opus opus-devel curl wget git
```

### OpenSUSE

```sh
sudo zypper install gcc make automake openssl-devel openssl-1_1  \
libffi-devel python311-devel python311-libnacl opus libopus0 wget git curl
```

### Arch

```sh
sudo pacman -S --needed base-devel openssl openssl-1.1 libffi python python-libnacl opus
```

### MacOS

```sh
brew install openssl openssl@1.1 libffi git curl make opus
```