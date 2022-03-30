# Contributing

We are glad that you're willing to contribute to this project. We are usually very lenient and relaxed with the submissions of PRs, and Issues reports. But there are some stuff that you need to know before contributing.

## Requirements

To get started, you'll need these things installed: 

- [Git](https://git-scm.com/)
- [Python 3.10](https://www.python.org/)
- [Pipenv](https://pipenv.pypa.io/en/latest/)
- [WSL](https://docs.microsoft.com/en-us/windows/wsl/) (If working on Windows)

## Installing Dependencies

Getting the environment set up for the bot is a kinda complex process. Rin now uses [Uvloop](https://github.com/MagicStack/uvloop), which is a drop-in replacement for [Asyncio](https://docs.python.org/3/library/asyncio.html) and is just as fast as Node.js. If you want to get set up, here are the instructions to do so:

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

## Pull Requests and Commits

You have 2 option: Fork the repo and make a pull request back into the main one, or commit to the branch directly. Option 2 is preferred. **If it's not for any fixes including any hotfixes, please submit it to the dev branch, not the master branch**

## Formatting

This projects uses a ton of linters and formatters. The main formatters are Black, AutoPEP8, AutoFlake and Isort. And there are a lot of linters as well. Most of them are from Codefactor, Codacy, and Deepsource. You don't have to worry about them because they are set up as formatters on the CI/CD workflow. Meaning that once it is done, all the code is formatted already.

## Patches

In order to prevent merge conflicts for the upstream project [Kumiko](https://github.com/No767/Kumiko), all major changes for Rin needs to be added as a patch file (make sure that you make the commit first). To create one, run this cmd:

```sh
git format-patch [commit-hash] -1 --start-number=[insert-number-here] -o ./Patches/[commit-name]
```

Make sure that it is either outputting it to the `Patches` directory, or that you are in the `Patches` directory. This will create a patch file, and you can use that to push to the main repo. From downstream, this cmd can be run:

```sh
git apply [patch file]
```

This allows for synchronization between both projects without constantly creating merge conflicts. Make sure that this is for the main code changes, not for other files like `README.md` or `LICENSE`.
## Issue and Feature Requests Reports

If there is an issue or a feature you want to be added, use the built-in GitHub issue tracker. Though a system like Jira could be used, it would be more efficient to just use the issue tracker that GitHub provides. 

- If submitting a issue report, follow the template. Duplicates will not receive support
- If submitting a feature request, follow the template as well. As with issue reports, duplicate requests will not receive support

# Releasing Tags
In order to automate the release system, you have to make sure that in order to use it, the git commit message must be done correctly. Only use this if there is a new update that is ready to be released. These are pretty similar to [Angular's Commit Message Conventions](https://github.com/angular/angular.js/blob/master/DEVELOPERS.md#-git-commit-guidelines). Here's a table that should help with explaining this:

| Type of Release, Update, or Patch | Example |
|              :--:                 | :--:    | 
| Major Release                     | `Release: v2.5` | 
| Minor Release                     | `Update: v2.5.1`|
| Patch Release                     | `Fix: Instagram API Cog removal` |


## Git Commit StyleGuides

- If updating any other files that aren't project files or not important (stuff like README.md, contributing.md, etc), add the [skip ci] label in the front
- With each new commit, the message should be more or less describing the changes. Please don't write useless commit messages...
- If releasing tags, have it in this style. `Release: [insert what changed here]`, `Update: [insert what changed here]`, and `Fix: [insert what changed here]`. Release is a major release. This means it bumps from 1.0 to 2.0. Minor means it bumps up the version from 1.4 to 1.4.1 for example. And fix just applies a patch, which would be 1.4.1 to 1.4.1.1.
