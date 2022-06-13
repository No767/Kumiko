<div align=center>

# Rin

![Rin's Logo](./assets/Rin-Trans-Logo-V0.1.0.png)

<br/>

![GitHub Pipenv locked Python version (branch)](https://img.shields.io/github/pipenv/locked/python-version/No767/Rin/dev?label=Python&logo=python&logoColor=white) 
[![CodeQL](https://github.com/No767/Rin/actions/workflows/codeql-analysis.yml/badge.svg?branch=dev)](https://github.com/No767/Rin/actions/workflows/codeql-analysis.yml) [![Snyk](https://github.com/No767/Rin/actions/workflows/snyk.yml/badge.svg?branch=dev)](https://github.com/No767/Rin/actions/workflows/snyk.yml) [![Codacy Badge](https://app.codacy.com/project/badge/Grade/ec2cf4ceacc746b3a4570d324c843a4b)](https://www.codacy.com/gh/No767/Rin/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=No767/Rin&amp;utm_campaign=Badge_Grade) [![Open in GitPod](https://img.shields.io/badge/Open%20in%20-GitPod-blue?logo=gitpod)](https://gitpod.io/#https://github.com/No767/Rin) ![GitHub release (latest by date)](https://img.shields.io/github/v/release/No767/Rin?label=Release&logo=github) ![GitHub](https://img.shields.io/github/license/No767/Rin?label=License&logo=github)

A Discord bot focused on obtaining data from third-party services with lighting performance in mind

<div align=left>

# Info

Rin is a Discord bot written with Pycord and Python, and is focused on fetching data from third-party services with lighting performance in mind. For example, you could look up some memes with the Reddit service, 
or find your favorite anime with the MyAnimeList service. Rin supports a lot of services, such as Twitter, MangaDex, Reddit, YouTube, DeviantArt, Hypixel, and many more. Rin is also designed to be fast, and uses [Uvloop](https://github.com/MagicStack/uvloop) under the 
hood, which is 2 times faster than Node.js and reaches the same speeds as many Go programs. On top on that, Rin is powered by the fatest JSON parser in the world, SIMDJSON. For more info, please check out the [Docs](https://docs.rinbot.live/).

## Modularity

Rin is designed to be modular, where you can remove cogs, or add new ones. In fact, you can build your entire bot on top of Rin, and [Kumiko](https://github.com/No767/Kumiko) basically does that. However, if you want to build your bot on top of Rin, you have to cite the bot as a fork of Rin (you are essentially using a fork of Rin if you decide to do so), link back the GitHub repo in somewhere that people will notice, and give credit to the original developer (which is me, No767).

# Prefix

Rin's prefix is `/`.

# Inviting the Bot

Via Top.gg, or any of the links in the [Bot Discovery Network](https://github.com/No767/Rin#bot-discovery-network-links) section. You can invite Rin by clicking [here](https://top.gg/bot/865883525932253184/invite). Note that previously (before v2.0.0), the prefix was `.`. Versions beyond v2.0.0 will only support the slash (`/`) prefix.

# Installing Dependencies

Getting the environment set up for the bot is a kinda complex process. Rin now uses [Uvloop](https://github.com/MagicStack/uvloop), which is a drop-in replacement for [Asyncio](https://docs.python.org/3/library/asyncio.html) and is just as fast as Node.js. If you want to get set up, here are the instructions to do so:

## Windows 

1. Install [WSL2](https://docs.microsoft.com/en-us/windows/wsl/). Pick your distro of choice. In this example, we will use Ubuntu 22.04
2. Install the suggested build dependencies for pyenv. 

    ```sh
    sudo apt-get update; sudo apt-get install make build-essential libssl-dev zlib1g-dev \
    libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm \
    libncursesw5-dev xz-utils tk-dev libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev python3.10-dev git
    ```

3. Install Pyenv. Also make sure to follow the instructions [here](https://github.com/pyenv/pyenv#set-up-your-shell-environment-for-pyenv)

    ```sh
    curl https://pyenv.run | bash
    pyenv update
    pyenv install 3.10.5
    pyenv global 3.10.5
    pyenv rehash
    ```

4. Restart your shell (make sure you have added it to your path and configured it either in your `.zshrc`, or `.bashrc` files)
    
    ```sh
    exec "$SHELL"
    ```

5. Fork and clone the repo

    ```sh
    git clone https://github.com/[username]/Rin.git && cd Rin
    ```


6. Run Make to create the venv and install dependencies

    ```sh
    make dev-setup
    ```

## Linux
    
### Ubuntu

1. Install the suggested build dependencies for pyenv. 

    ```sh
    sudo apt-get update; sudo apt-get install make build-essential libssl-dev zlib1g-dev \
    libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm \
    libncursesw5-dev xz-utils tk-dev libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev python3.10-dev git
    ```

2. Install Pyenv. Also make sure to follow the instructions [here](https://github.com/pyenv/pyenv#set-up-your-shell-environment-for-pyenv)

    ```sh
    curl https://pyenv.run | bash
    pyenv update
    pyenv install 3.10.5
    pyenv global 3.10.5
    pyenv rehash
    ```

3. Restart your shell (make sure you have added it to your path and configured it either in your `.zshrc`, or `.bashrc` files)
    
    ```sh
    exec "$SHELL"
    ```

4. Fork and clone the repo

    ```sh
    git clone https://github.com/[username]/Rin.git && cd Rin
    ```

5. Run Make to create the venv and install dependencies

    ```sh
    make dev-setup
    ```

### OpenSUSE

1. Install the suggested build dependencies for pyenv.

    ```sh
    sudo zypper install gcc automake bzip2 libbz2-devel xz xz-devel openssl-devel ncurses-devel \
    readline-devel zlib-devel tk-devel libffi-devel sqlite3-devel python310-devel
    ```

2. Install Pyenv. Also make sure to follow the instructions [here](https://github.com/pyenv/pyenv#set-up-your-shell-environment-for-pyenv)

    ```sh
    curl https://pyenv.run | bash
    pyenv update
    pyenv install 3.10.5
    pyenv global 3.10.5
    pyenv rehash
    ```

3. Restart your shell (make sure you have added it to your path and configured it either in your `.zshrc`, or `.bashrc` files)
    
    ```sh
    exec "$SHELL"
    ```

4. Fork and clone the repo

    ```sh
    git clone https://github.com/[username]/Rin.git && cd Rin
    ```

5. Run Make to create the venv and install dependencies

    ```sh
    make dev-setup
    ```

### Fedora/CentOS

1. Install the suggested build dependencies for pyenv

    Fedora 22 and above:

    ```sh
    sudo dnf install make gcc zlib-devel bzip2 bzip2-devel readline-devel sqlite sqlite-devel openssl-devel tk-devel libffi-devel xz-devel python-devel git curl
    ```

    CentOS or Fedora 22 and below:

    ```sh
    sudo yum install gcc zlib-devel bzip2 bzip2-devel readline-devel sqlite sqlite-devel openssl-devel tk-devel libffi-devel xz-devel python-devel git curl
    ```

2. Install Pyenv. Also make sure to follow the instructions [here](https://github.com/pyenv/pyenv#set-up-your-shell-environment-for-pyenv)

    ```sh
    curl https://pyenv.run | bash
    pyenv update
    pyenv install 3.10.5
    pyenv global 3.10.5
    pyenv rehash
    ```

3. Restart your shell (make sure you have added it to your path and configured it either in your `.zshrc`, or `.bashrc` files)
    
    ```sh
    exec "$SHELL"
    ```

4. Fork and clone the repo

    ```sh
    git clone https://github.com/[username]/Rin.git && cd Rin
    ```

5. Run Make to create the venv and install dependencies

    ```sh
    make dev-setup
    ```
### Arch/Manjaro

1. Install the suggested build dependencies for pyenv

    ```sh
    sudo pacman -S --needed base-devel openssl zlib xz tk python libffi
    ```

2. Install Pyenv. Also make sure to follow the instructions [here](https://github.com/pyenv/pyenv#set-up-your-shell-environment-for-pyenv)

    ```sh
    curl https://pyenv.run | bash
    pyenv update
    pyenv install 3.10.5
    pyenv global 3.10.5
    pyenv rehash
    ```

3. Restart your shell (make sure you have added it to your path and configured it either in your `.zshrc`, or `.bashrc` files)
    
    ```sh
    exec "$SHELL"
    ```

4. Fork and clone the repo

    ```sh
    git clone https://github.com/[username]/Rin.git && cd Rin
    ```

5. Run Make to create the venv and install dependencies

    ```sh
    make dev-setup
    ```

## MacOS

1. Install Xcode Command Line Tools (`xcode-select --install`) and [Homebrew](https://brew.sh/)

2. Install the suggested build dependencies for pyenv

    ```sh
    brew install openssl readline sqlite3 xz zlib tcl-tk git curl make
    ```
3. Install Pyenv via Homebrew

    ```sh
    brew update
    brew install pyenv
    ```

4. Install Python

    ```sh
    pyenv update
    pyenv install 3.10.5
    pyenv global 3.10.5
    pyenv rehash
    ```

5. Follow the rest of the steps, starting on [Set Up Your shell Environment For Pyenv](https://github.com/pyenv/pyenv#set-up-your-shell-environment-for-pyenv)

5. Fork and clone the repo

    ```sh
    git clone https://github.com/[username]/Rin.git && cd Rin
    ```

6. Run Make to create the venv and install dependencies

    ```sh
    make dev-setup
    ```

# Licensing

All of Rin's code is licensed under Apache-2.0

# Contributing

See [Contributing](https://github.com/No767/Rin/blob/dev/Community/contributing.md)

# Links 

- [Documentation](https://docs.rinbot.live)
- [Website](https://rinbot.live)
- [Status Tracker](https://status.rinbot.live)
    
## Bot Discovery Network Links
    
- [Top.gg](https://top.gg/bot/865883525932253184)
- [Discords.com](https://discords.com/bots/bot/865883525932253184)
- [Discord.bots.gg](https://discord.bots.gg/bots/865883525932253184)
- [Discordlist.space](https://discordlist.space/bot/865883525932253184)


<div align=center>
    
 [![Bots for Discord](https://discords.com/bots/api/bot/865883525932253184/widget)](https://discords.com/bots/bots/865883525932253184)
 [![Top.gg](https://top.gg/api/widget/865883525932253184.svg)](https://top.gg/bot/865883525932253184)
 [![DiscordList.space](https://api.discordlist.space/v2/bots/865883525932253184/widget?background=7289DA&radius=12)](https://discordlist.space/bot/865883525932253184)   
</div>
