# Contributing

We are glad that you're willing to contribute to this project. We are usually very lenient and relaxed with the submissions of PRs, and Issues reports. But there are some stuff that you need to know before contributing.

## Requirements

To get started, you'll need these things installed: 

- Git
- Python 3.10 or higher
- Pipenv

## Installing Dependencies

All of the dependencies that is needed for this project can be found within the `requirements.txt` within the root directory of this project. Git can be found [here](https://git-scm.com/). Python can be also found at its website ([Python's Official Website](https://www.python.org/)).

You have 2 options on how you want to install the dependencies: via [Pip](https://pypi.org) or via [Pipenv](https://pipenv.pypa.io/en/latest/). Pipenv is recommended over pip for this repo.

**Option 1**: Via [Pip](https://pypi.org)

`pip install --upgrade pip setuptools wheel` 

`pip install -r requirements.txt`

**Option 2**: Via [Pipenv](https://pipenv.pypa.io/en/latest/)

`pipenv install`

## Pull Requests and Commits

You have 2 option: Fork the repo and make a pull request back into the main one, or commit to the branch directly. Option 2 is preferred. **If it's not for any fixes including any hotfixes, please submitting it to the dev branch, not the master branch**

## Formatting

This projects uses a ton of linters and formatters. The main formatters are Black, AutoPEP8, and Isort. And there are a lot of linters as well. Most of them are from Codefactor, Codacy, and Deepsource. You don't have to worry about them because they are set up as formatters on the CI/CD workflow. Meaning that once it is done, all the code is formatted already.
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

## Code StyleGuides

- Use the PEP 8 Standard if possible

