<div align=center>

# Kumiko

<img src="./assets/kumiko.jpg" width=200 height=200>

<br>

![GitHub Pipenv locked Python version (branch)](https://img.shields.io/github/pipenv/locked/python-version/No767/Rin/dev?label=Python&logo=python&logoColor=white)
[![CodeQL](https://github.com/No767/Kumiko/actions/workflows/codeql-analysis.yml/badge.svg?branch=dev)](https://github.com/No767/Kumiko/actions/workflows/codeql-analysis.yml) [![Snyk](https://github.com/No767/Kumiko/actions/workflows/snyk.yml/badge.svg?branch=dev)](https://github.com/No767/Kumiko/actions/workflows/snyk.yml) [![Format](https://github.com/No767/Kumiko/actions/workflows/format.yml/badge.svg?branch=dev)](https://github.com/No767/Kumiko/actions/workflows/format.yml) [![Codacy Badge](https://app.codacy.com/project/badge/Grade/950cd812f1e04f0d813bb0298fdaa225)](https://www.codacy.com/gh/No767/Kumiko/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=No767/Kumiko&amp;utm_campaign=Badge_Grade) ![GitHub release (latest by date)](https://img.shields.io/github/v/release/No767/Kumiko?display_name=tag&label=Release&logo=github) ![GitHub](https://img.shields.io/github/license/No767/Rin?label=License&logo=github)

The Multipurpose Version of [Rin](https://github.com/No767/Rin) - Supports Moderation, Economy, and much much more

<div align=left>

# Inviting the Bot

Still in early production. Not ready for release yet

# Getting Started (For Developers)

Getting the environment set up for Kumiko is a kinda complex process. Kumiko now uses [Uvloop](https://github.com/MagicStack/uvloop), which is a drop-in replacement for [Asyncio](https://docs.python.org/3/library/asyncio.html) and is just as fast as Node.js. If you want to get set up, here are the instructions to do so:
## Windows

1. Install [WSL2](https://docs.microsoft.com/en-us/windows/wsl/). Uvloop does not have Windows support nor does the owner want to add it.
2. Make sure to install LZMA (If on Debian/Ubuntu) and all other needed libs. The `Jamdict-Data` package requires it to unpack the SQLite3 DB. To do so, run this command:

```sh
sudo apt-get install liblzma-dev lzma python3.10-dev
```

3. Compile Python 3.10 from source (or install it with your package manager). If you need a guide, [here's](https://realpython.com/installing-python/#how-to-build-python-from-source-code) one. Note that this guide is for Ubuntu 20.04, so depending on your distro, it may be different.
4. Install [Pipenv](https://pipenv.readthedocs.io/en/latest/). To do so, run this command:

```sh
sudo python3.10 -m pip install --upgrade pipenv
```

5. Clone this repo.
6. Create the Pipenv. To do so, run this command: 

```sh
pipenv --python 3.10
```

7. `cd` into the cloned repo and install all the dependencies by running this command:

```sh
pipenv install
```
8. (Optional) If you are using PyCharm, make sure to set the Python Interpreter to WSL and specify the Python interpreter to use. For this, the file path will be usually here:

```sh
$HOME/.local/share/virtualenvs/[Project Name]/bin/python3.10
```

Or if you using VS Code, install the [WSL](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-wsl) Extension for VS Code, and follow steps 1-7. Then connect to WSL, and select the repo as a folder to open. 

## Linux

1. Make sure to install LZMA (If on Debian/Ubuntu) and all other needed libs. The `Jamdict-Data` package requires it to unpack the SQLite3 DB. To do so, run this command:

```sh
sudo apt-get install liblzma-dev lzma python3.10-dev
```

If you are on a different distro that doesn't use `apt` like CentOS, install LZMA like so: 

```sh
yum install -y xz-devel
```

2. Compile Python 3.10 from source (or install it with your package manager). If you need a guide, [here's](https://realpython.com/installing-python/#how-to-build-python-from-source-code) one. 
3. Install [Pipenv](https://pipenv.readthedocs.io/en/latest/). To do so, run this command:

```sh
sudo python3.10 -m pip install --upgrade pipenv
```

4. Clone this repo.
5. Create the Pipenv. To do so, run this command: 

```sh
pipenv --python 3.10
```

6. `cd` into the cloned repo and install all the dependencies by running this command:

```sh
pipenv install
```

## MacOS

**Note that I have not tested MacOS yet. If you find any errors, please let me know by submitting a GitHub Issue Report.**

1. Install Python 3.10. This can be installed with the installer or compiled from source (Or use Homebrew). Either way it doesn't matter. 
2. Install [Pipenv](https://pipenv.readthedocs.io/en/latest/). To do so, run this command:

```sh
python -m pip install --upgrade pipenv
```

3. Clone this repo. 
4. Create the Pipenv. To do so, run this command: 

```sh
pipenv --python 3.10
```

5. `cd` into the cloned repo and install all the dependencies by running this command:

```sh
pipenv install
```

# Licensing

Kumiko and Rin are both licensed under Apache-2.0. This project uses some of the cogs from EasyBot.py and its plugins. All EasyBot.py and EasyBot-Plugin code is licensed under CC0-1.0, and all private code changes is licensed under Apache-2.0. 

# Contributing

See [Contributing](https://github.com/No767/Kumiko/blob/master/Community/contributing.md)
