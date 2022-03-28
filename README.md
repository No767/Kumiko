<div align=center>

# Rin

<img src="./assets/Rin Logo V4 (GitHub).png">

<br/>

![GitHub Pipenv locked Python version (branch)](https://img.shields.io/github/pipenv/locked/python-version/No767/Rin/dev?label=Python&logo=python&logoColor=white) [![Top.gg Status](https://top.gg/api/widget/status/865883525932253184.png)](https://top.gg/bot/865883525932253184) 
[![CodeQL](https://github.com/No767/Rin/actions/workflows/codeql-analysis.yml/badge.svg?branch=dev)](https://github.com/No767/Rin/actions/workflows/codeql-analysis.yml) [![Snyk](https://github.com/No767/Rin/actions/workflows/snyk.yml/badge.svg?branch=dev)](https://github.com/No767/Rin/actions/workflows/snyk.yml) [![Format](https://github.com/No767/Rin/actions/workflows/format.yml/badge.svg?branch=dev)](https://github.com/No767/Rin/actions/workflows/format.yml) [![Codacy Badge](https://app.codacy.com/project/badge/Grade/ec2cf4ceacc746b3a4570d324c843a4b)](https://www.codacy.com/gh/No767/Rin/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=No767/Rin&amp;utm_campaign=Badge_Grade) [![Open in GitPod](https://img.shields.io/badge/Open%20in%20-GitPod-blue?logo=gitpod)](https://gitpod.io/#https://github.com/No767/Rin) ![GitHub release (latest by date)](https://img.shields.io/github/v/release/No767/Rin?label=Release&logo=github) ![GitHub](https://img.shields.io/github/license/No767/Rin?label=License&logo=github)

A Discord bot focused on obtaining data from third-party services with lighting performance in mind

<div align=left>

# Info

Rin is a Discord bot written with Pycord and Python, and is focused on fetching data from third-party services with lighting performance in mind. For example, you could look up some memes with the Reddit service, 
or find your favorite anime with the MyAnimeList service. Rin supports a lot of services, such as Twitter, MangaDex, Reddit, YouTube, DeviantArt, Hypixel, and many more. Rin is also designed to be fast, and uses [Uvloop](https://github.com/MagicStack/uvloop) under the 
hood, which is 2 times faster than Node.js and reaches the same speeds as many Go programs. For more info, please check out the [Docs](https://docs.rinbot.live/).

# Prefix

Rin's prefix is `/`.

# Inviting the Bot

Via Top.gg, or any of the links in the [Bot Discovery Network](https://github.com/No767/Rin#bot-discovery-network-links) section. You can invite Rin by clicking [here](https://top.gg/bot/865883525932253184/invite). Note that previously (before v2.0.0), the prefix was `.`. Versions beyond v2.0.0 will only support the slash (`/`) prefix.

# Installing Dependencies
Getting the environment set up for the bot is a kinda complex process. Rin now uses [Uvloop](https://github.com/MagicStack/uvloop), which is a drop-in replacement for [Asyncio](https://docs.python.org/3/library/asyncio.html) and is just as fast as Node.js. Note that soon Rin will be using RustPython instead. If you want to get set up, here are the instructions to do so:

## Windows

1. Install [WSL2](https://docs.microsoft.com/en-us/windows/wsl/). Uvloop does not have Windows support nor does the owner want to add it. (These instructions use Ubuntu as the main distro. If you want to build and develop Rin on a different distro, look ahead into the Linux section)
2. Add the `software-properties-common` package first. This is required for getting `python3.10-dev` (which is the Python C Header files, required by Pycord for voice support). To do this, run this cmd:

    ```sh
    sudo apt-get install software-properties-common
    ```
    
3. Make sure to install the needed packages. To do so, run this command:

    ```sh
    sudo apt-get install liblzma-dev lzma libffi-dev python3.10-dev
    ```

4. Install Python 3.10. Chances are the `python3.10-dev` package requires Python 3.10 as a dependency, so make sure Python 3.10 is installed. If you did it this way, you will more than likely need to get pip, and you will need to use the get-pip.py method to do so. 

5. **Skip this step if you already have pip configured and installed for Python 3.10. Run `pip3.10 --version` to check if it is installed for Python 3.10**. Chances are that you don't have pip installed for Python 3.10. So you can use either cURL or wget in order to download it. In order to do so, run this cmd:

    cURL:

    ```sh
    curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py && python3.10 get-pip.py
    ```

    wget: 

    ```sh
    wget https://bootstrap.pypa.io/get-pip.py && python3.10 get-pip.py
    ```

    After doing so, make sure to run `pip3.10 --version` to double check if it is installed correctly.

6. Install [Pipenv](https://pipenv.readthedocs.io/en/latest/). To do so, run this command:

    ```sh
    sudo python3.10 -m pip install --upgrade pipenv
    ```

7. Create a fork of this repo, and then clone your fork of the repo. If you need the cmd to do so, run this cmd:

    ```sh
    git clone https://github.com/[your github username]/Rin.git
    ```

8. `cd` into the cloned repo and set up the pipenv enviroment. To do so, run this cmd:

    ```sh
    cd Rin && pipenv --python 3.10
    ```

9. And now finally install all the dependencies by running this command:

    ```sh
    pipenv install
    ```

10. (Optional) If you are using PyCharm, make sure to set the Python Interpreter to WSL and specify the Python interpreter to use. For this, the file path will be usually here:

    ```sh
    $HOME/.local/share/virtualenvs/[Project Name]/bin/python3.10
    ```

Or if you using VS Code, install the [WSL](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-wsl) Extension for VS Code, and follow steps 1-6. Then connect to WSL. 

## Linux

### Ubuntu
    
1. Add the `software-properties-common` package first. This is required for getting `python3.10-dev` (which is the Python C Header files, required by Pycord for voice support). To do this, run this cmd:

    ```sh
    sudo apt-get install software-properties-common
    ```
    
2. Install all of the needed packages. To do so, run this command:

    ```sh
    sudo apt-get install liblzma-dev lzma libffi-dev python3.10-dev
    ```


4. Install Python 3.10. Chances are the `python3.10-dev` package requires Python 3.10 as a dependency, so make sure Python 3.10 is installed. If you did it this way, you will more than likely need to get pip, and you will need to use the get-pip.py method to do so. 

5. **Skip this step if you already have pip configured and installed for Python 3.10. Run `pip3.10 --version` to check if it is installed for Python 3.10**. Chances are that you don't have pip installed for Python 3.10. So you can use either cURL or wget in order to download it. In order to do so, run this cmd:

    cURL:

    ```sh
    curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py && python3.10 get-pip.py
    ```

    wget: 

    ```sh
    wget https://bootstrap.pypa.io/get-pip.py && python3.10 get-pip.py
    ```

    After doing so, make sure to run `pip3.10 --version` to double check if it is installed correctly.

6. Install [Pipenv](https://pipenv.readthedocs.io/en/latest/). To do so, run this command:

    ```sh
    sudo python3.10 -m pip install --upgrade pipenv
    ```

7. Clone this repo. If you need the cmd to do so, run this cmd:

    ```sh
    git clone https://github.com/No767/Rin.git
    ```

8. `cd` into the cloned repo and set up the pipenv enviroment. To do so, run this cmd:

    ```sh
    cd Rin && pipenv --python 3.10
    ```

9. And now finally install all the dependencies by running this command:

    ```sh
    pipenv install
    ```

### OpenSUSE

1. Make sure to install the required packages for voice support. 

   ```sh
   sudo zypper install python310-devel libffi-devel xz-level libopenssl-devel libopenssl-1_1-devel git 
   ```

2. Install Python 3.10. You also have the choice of compiling it, but make sure you also have OpenSSL installed and all other required modules

   ```sh
   sudo zypper install python310
   ```

3. **Skip this step if you already have `pip3.10` installed. To check, run `pip3.10 --version`** Install Pip via either the `ensurepip` module or via the `get-pip.py` method

   ensurepip: 

   ```sh
   python3.10 -m ensurepip
   ```
    cURL (for `get-pip.py`):

    ```sh
    curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py && python3.10 get-pip.py
    ```

    wget (for `get-pip.py`): 

    ```sh
    wget https://bootstrap.pypa.io/get-pip.py && python3.10 get-pip.py
    ```

4. Install [Pipenv](https://pipenv.readthedocs.io/en/latest/). To do so, run this command:

   ```sh
   sudo python3.10 -m pip install --upgrade pipenv 
   ```

5. Go to GitHub and Fork the main repo. Then clone your fork of the repo:

   ```sh
   git clone https://github.com/[your github username]/Rin
   ```

6. `cd` into your newly created fork and create the env that you will be using

   ```sh
   pipenv --python 3.10
   ```

7. Install all dependencies. More than likely you will face an error installing cChardet. So just run `pipenv install cchardet` to reinstall it and it should do the trick

   ```sh
   pipenv install
   ```

8. (Optional) Create a shell by running the cmd below:

   ```sh
   pipenv shell
   ```

### Fedora/CentOS

1. Make sure you installed the required libs (if you are using CentOS, you may have to use `yum` instead of `dnf`). To do so, run this cmd:

    ```sh
    sudo dnf -y groupinstall "Development Tools"
    ```
   
    ```sh
    sudo dnf install python310-devel libffi-devel openssl-devel xz-devel gcc bzip2-devel git
    ```
2. Install Python 3.10. You also have the choice of compiling it, but make sure you also have OpenSSL installed and all other required modules before compiling

   ```sh
   sudo dnf install python3.10
   ```

3. **Skip this step if you already have `pip3.10` installed. To check, run `pip3.10 --version`** Install Pip via either the `ensurepip` module or via the `get-pip.py` method

   ensurepip: 

   ```sh
   python3.10 -m ensurepip
   ```
    cURL (for `get-pip.py`):

    ```sh
    curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py && python3.10 get-pip.py
    ```

    wget (for `get-pip.py`): 

    ```sh
    wget https://bootstrap.pypa.io/get-pip.py && python3.10 get-pip.py

4. Install [Pipenv](https://pipenv.readthedocs.io/en/latest/). To do so, run this command:

   ```sh
   sudo python3.10 -m pip install --upgrade pipenv 
   ```

5. Go to GitHub and Fork the main repo. Then clone your fork of the repo:

   ```sh
   git clone https://github.com/[your github username]/Rin
   ```

6. `cd` into your newly created fork and create the env that you will be using

   ```sh
   pipenv --python 3.10
   ```

7. Install all dependencies. More than likely you will face an error installing cChardet. So just run `pipenv install cchardet` to reinstall it and it should do the trick

   ```sh
   pipenv install
   ```

8. (Optional) Create a shell by running the cmd below:

   ```sh
   pipenv shell
   ```
## MacOS

**Note that I have not tested MacOS yet. If you find any errors, please let me know by submitting a GitHub Issue Report.**

1. Install Python 3.10. This can be installed with the installer or compiled from source (Or use Homebrew). Either way it doesn't matter. 
2. Install [Pipenv](https://pipenv.readthedocs.io/en/latest/). To do so, run this command:

    ```sh
    python -m pip install --upgrade pipenv
    ```

3. Create a fork of this repo and clone it.

4. `cd` into the cloned repo and create the Pipenv. To do so, run this command: 

    ```sh
    cd Rin && pipenv --python 3.10
    ```

5. And now install all the dependencies by running this command:

    ```sh
    pipenv install
    ```

# Licensing

Rin is licensed under Apache-2.0. This project uses some of the cogs from EasyBot.py and its plugins. All EasyBot.py and EasyBot-Plugin code is licensed under CC0-1.0, and all private code changes is licensed under Apache-2.0. 

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
