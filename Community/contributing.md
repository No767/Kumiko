# Contributing

We are glad that you're willing to contribute to this project. We are usually very lenient and relaxed with the submissions of PRs, and Issues reports. But there are some stuff that you need to know before contributing.

## Requirements

To get started, you'll need these things installed: 

- Git
- Python 3.10.x
- Pipenv

## Installing Dependencies

All of the dependencies can be found within `Pipfile` and `Pipfile.lock`, and requires Pipenv in order to be installed.  Git can be found [here](https://git-scm.com/). Python can be also found at its website ([Python's Official Website](https://www.python.org/)). Pipenv can be found [here](https://pipenv.pypa.io/en/latest).

Your only option is via [Pipenv](https://pipenv.pypa.io/en/latest/)

`pipenv install`

If you haven't set up the environment yet, run this in the root directory of the git repo:

`pipenv --python 3.10`

## Uvloop 

Rin will start using uvloop as a replacement for asyncio, and uvloop can reach speeds similar to Node.js. For developing, follow the prompts below:

### Windows 

1. Install WSL2 
2. Install Python 3.10.x (Compile it from the source). If you need help, refer to the [docs](https://docs.python.org/3/using/unix.html) or this [article](https://computingforgeeks.com/how-to-install-python-on-ubuntu-linux-system/)
3. Make sure that Python and Pip are now using the Python 3.10.x version. You may also want to set aliases for them at this stage
4. Install Pipenv
5. Run `pipenv --python 3.10`
6. Install All Dependencies 

If you want to execute the code, make sure to run it with Bash or WSL instead.

### Linux

1. Compile Python 3.10.x from source. If you need help, refer to the [docs](https://docs.python.org/3/using/unix.html) or this [article](https://computingforgeeks.com/how-to-install-python-on-ubuntu-linux-system/)
2. Make sure that Python and Pip are now using the Python 3.10.x version. You may also want to set aliases for them at this stage
3. Install Pipenv
4. Run `pipenv --python 3.10`
5. Install All Dependencies


### MacOS

1. Install Python 3.10.x
2. Install Pipenv
3. Run `pipenv --python 3.10`
4. Install All Dependencies
 
## Pull Requests and Commits

You have 2 option: Fork the repo and make a pull request back into the main one, or commit to the branch directly. Option 2 is preferred. **If it's not for any fixes including any hotfixes, please submit it to the dev branch, not the master branch**

## Formatting

This projects uses a ton of linters and formatters. The main formatters are Black, AutoPEP8, AutoFlake and Isort. And there are a lot of linters as well. Most of them are from Codefactor, Codacy, and Deepsource. You don't have to worry about them because they are set up as formatters on the CI/CD workflow. Meaning that once it is done, all the code is formatted already.

## Patches

In order to prevent merge conflicts for the upstream project [Kumiko](https://github.com/No767/Kumiko), all major changes for Rin needs to be added as a patch file (make sure that you make the commit first). To create one, run this cmd:

```sh
git format-patch -1 -o ./Patches
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
