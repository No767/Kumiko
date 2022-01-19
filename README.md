<div align=center>

# Rin

<img src="./assets/Rin Logo V4 (GitHub).png">

<br/>

![GitHub Pipenv locked Python version (branch)](https://img.shields.io/github/pipenv/locked/python-version/No767/Rin/dev?label=Python&logo=python&logoColor=white) [![Top.gg Status](https://top.gg/api/widget/status/865883525932253184.png)](https://top.gg/bot/865883525932253184) 
[![CodeQL](https://github.com/No767/Rin/actions/workflows/codeql-analysis.yml/badge.svg?branch=dev)](https://github.com/No767/Rin/actions/workflows/codeql-analysis.yml) [![Snyk](https://github.com/No767/Rin/actions/workflows/snyk.yml/badge.svg?branch=dev)](https://github.com/No767/Rin/actions/workflows/snyk.yml) [![Format](https://github.com/No767/Rin/actions/workflows/format.yml/badge.svg?branch=dev)](https://github.com/No767/Rin/actions/workflows/format.yml) [![Codacy Badge](https://app.codacy.com/project/badge/Grade/ec2cf4ceacc746b3a4570d324c843a4b)](https://www.codacy.com/gh/No767/Rin/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=No767/Rin&amp;utm_campaign=Badge_Grade) ![GitHub release (latest by date)](https://img.shields.io/github/v/release/No767/Rin?label=Release&logo=github) ![GitHub](https://img.shields.io/github/license/No767/Rin?label=License&logo=github)

A Discord bot focused on obtaining data from third-party services

<div align=left>

# Inviting the Bot

Via Top.gg. You can invite Rin by clicking [here](https://top.gg/bot/865883525932253184/invite)

# Building

Getting the environment set up for the bot is a kinda complex process. Rin now uses [Uvloop](https://github.com/MagicStack/uvloop), which is a drop-in replacement for [Asyncio](https://docs.python.org/3/library/asyncio.html) and is just as fast as Node.js. If you want to get set up, here are the instructions to do so:
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

Or if you using VS Code, install the [WSL](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-wsl) Extension for VS Code, and follow steps 1-6. Then connect to WSL. 

## Linux

1. Make sure to install LZMA (If on Debian/Ubuntu). The `Jamdict-Data` package requires it to unpack the SQLite3 DB. To do so, run this command:

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

Rin is licensed under Apache-2.0. This project uses some of the cogs from EasyBot.py and its plugins. All EasyBot.py and EasyBot-Plugin code is licensed under CC0-1.0, and all private code changes is licensed under Apache-2.0. 

# Contributing

See [Contributing](https://github.com/No767/Rin/blob/master/Community/contributing.md)

# Links 

- [Documentation](https://docs.rinbot.live)
- [Top.gg](https://top.gg/bot/865883525932253184)
- [Website](https://rinbot.live)
- [Status Tracker](https://status.rinbot.live)


<div align=center>
    
 [![Bots for Discord](https://discords.com/bots/api/bot/865883525932253184/widget)](https://discords.com/bots/bots/865883525932253184)
 [![Discord.boats](https://discord.boats/api/widget/865883525932253184?type=svg)](https://discord.boats/bot/865883525932253184) 
    
</div>
