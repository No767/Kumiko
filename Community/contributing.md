# Contributing

We are glad that you're willing to contribute to this project. We are usually very lenient and relaxed with the submissions of PRs, and Issues reports. But there are some stuff that you need to know before contributing.

## Requirements

To get started, you'll need these things installed: 

- Git
- Python 3.6 and above (Made in 3.9.6 and 3.9.7)

## Installing Dependencies

All of the dependencies that is needed for this project can be found within the `requirements.txt` within the root directory of this project. Git can be found [here](https://git-scm.com/). Python can be also found at its website ([Python's Official Website](https://www.python.org/)).

Before you can get working, you need to run 2 commands:

- `pip install --upgrade pip setuptools wheel`
- `pip install -r requirements.txt`

The reason why is that one of the dependencies breaks if setuptools and wheels is not updated. Make sure to do this in the root directory of this repo.

## Pull Requests and Commits

You have 2 option: Fork the repo and make a pull request back into the main one, or commit to the branch directly. Option 2 is preferred.

## Issue and Feature Requests Reports

If there is an issue or a feature you want to be added, use the built-in GitHub issue tracker. Though a system like Jira could be used, it would be more efficient to just use the issue tracker that GitHub provides. 

- If submitting a issue report, follow the template. Duplicates will not receive support
- If submitting a feature request, follow the template as well. As with issue reports, duplicate requests will not receive support

## Git Commit StyleGuides

- If updating any other files that aren't project files or not important, add the [skip ci] label in the front
- With each new commit, the message should be more or less describing the changes. Please don't write useless commit messages...

## Code StyleGuides

- Use the PEP 8 Standard if possible
- Use patches if possible (not needed, but if you want to, go ahead)
