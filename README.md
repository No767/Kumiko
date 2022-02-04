<div align=center>

# Rin

<img src="./assets/Rin Logo V4 (GitHub).png">

<br/>

![GitHub Pipenv locked Python version (branch)](https://img.shields.io/github/pipenv/locked/python-version/No767/Rin/dev?label=Python&logo=python&logoColor=white) [![Top.gg Status](https://top.gg/api/widget/status/865883525932253184.png)](https://top.gg/bot/865883525932253184) 
[![CodeQL](https://github.com/No767/Rin/actions/workflows/codeql-analysis.yml/badge.svg?branch=dev)](https://github.com/No767/Rin/actions/workflows/codeql-analysis.yml) [![Snyk](https://github.com/No767/Rin/actions/workflows/snyk.yml/badge.svg?branch=dev)](https://github.com/No767/Rin/actions/workflows/snyk.yml) [![Format](https://github.com/No767/Rin/actions/workflows/format.yml/badge.svg?branch=dev)](https://github.com/No767/Rin/actions/workflows/format.yml) [![Codacy Badge](https://app.codacy.com/project/badge/Grade/ec2cf4ceacc746b3a4570d324c843a4b)](https://www.codacy.com/gh/No767/Rin/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=No767/Rin&amp;utm_campaign=Badge_Grade) ![GitHub release (latest by date)](https://img.shields.io/github/v/release/No767/Rin?label=Release&logo=github) ![GitHub](https://img.shields.io/github/license/No767/Rin?label=License&logo=github)

A Discord bot focused on obtaining data from third-party services

<div align=left>

# Info

Rin is a Discord bot written with Pycord and Python, and is focused on fetching data from third-party services (for the more technical, this is done by contacting APIs). For example, you could look up some memes with the Reddit service, 
or find your favorite anime with the MyAnimeList service. Rin supports a lot of services, such as Twitter, MangaDex, Reddit, YouTube, DeviantArt, Hypixel, and many more. Rin is also designed to be fast, and uses [Uvloop](https://github.com/MagicStack/uvloop) under the 
hood, which is 2 times faster than Node.js and reaches the same speeds as many Go programs. For more info, please check out the [Docs](https://docs.rinbot.live/).

# Inviting the Bot

Via Top.gg. You can invite Rin by clicking [here](https://top.gg/bot/865883525932253184/invite)

# Installing Dependencies
Getting the environment set up for the bot is a kinda complex process. Rin now uses [Uvloop](https://github.com/MagicStack/uvloop), which is a drop-in replacement for [Asyncio](https://docs.python.org/3/library/asyncio.html) and is just as fast as Node.js. If you want to get set up, here are the instructions to do so:

## Windows

1. Install [WSL2](https://docs.microsoft.com/en-us/windows/wsl/). Uvloop does not have Windows support nor does the owner want to add it.
2. Add the `software-properties-common` package first. This is required for getting `python3.10-dev` (which is the Python C Header files, required by Pycord for voice support). To do this, run this cmd:

```sh
sudo apt-get install software-properties-common
```
    
3. Make sure to install LZMA (If on Debian/Ubuntu) and all other needed libs. The `Jamdict-Data` package requires it to unpack the SQLite3 DB. To do so, run this command:

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

8. `cd into the cloned repo and set up the pipenv enviroment. To do so, run this cmd:

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
    
1. Add the `software-properties-common` package first. This is required for getting `python3.10-dev` (which is the Python C Header files, required by Pycord for voice support). To do this, run this cmd:

```sh
sudo apt-get install software-properties-common
```
    
2. Make sure to install LZMA (If on Debian/Ubuntu). The `Jamdict-Data` package requires it to unpack the SQLite3 DB. To do so, run this command:

```sh
sudo apt-get install liblzma-dev lzma libffi-dev python3.10-dev
```

If you are on a different distro that doesn't use `apt` like CentOS, install LZMA like so: 

```sh
yum install -y xz-devel
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

8. `cd into the cloned repo and set up the pipenv enviroment. To do so, run this cmd:

```sh
cd Rin && pipenv --python 3.10
```

9. And now finally install all the dependencies by running this command:

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
4. `cd` into the cloned repo and create the Pipenv. To do so, run this command: 

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
- [Website](https://rinbot.live)
- [Status Tracker](https://status.rinbot.live)
    
## Bot Discovery Network Links
    
- [Top.gg](https://top.gg/bot/865883525932253184)
- [Discord.boats](https://discord.boats/bot/865883525932253184)
- [Discords.com](https://discords.com/bots/bot/865883525932253184)
- [Discord.bots.gg](https://discord.bots.gg/bots/865883525932253184)



<div align=center>
    
 [![Bots for Discord](https://discords.com/bots/api/bot/865883525932253184/widget)](https://discords.com/bots/bots/865883525932253184)
 [![Discord.boats](https://discord.boats/api/widget/865883525932253184?type=svg)](https://discord.boats/bot/865883525932253184) 
 [![Top.gg](https://top.gg/api/widget/865883525932253184.svg)](https://top.gg/bot/865883525932253184)
    
</div>
