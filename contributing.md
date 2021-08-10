# Requirements

To get started, you'll need these things installed: 

- Git 
- Python 3.6 or above
- Pip
- Discord.py
- Python-dotenv
- Cog Watch 

# Installing Dependencies

Git can be found [here](https://git-scm.com/). Python can be also found at its website ([Python's Official Website](https://www.python.org/)). And lastly, the Discord.py lib is listed within the requirements.txt file. 

To install the dependencies listed within the requirements.txt, just cd into the project's root directory and  run `pip install -r requirements.txt`.
Or you want to do it manually, run `pip install discord`, `pip install python-dotenv`, and `pip install cogwatch`.

# Pull Requests and Commits

You typically would want to fork the repo, and send all the changes back as a pull request. Though this is fine, it's more preferred to just to commit to the branch itself. The recommended way to do this is to send the pr or commit into the dev branch, then if it's stable enough, it'll be committed into the master branch.
# Git Commit StyleGuides

- Make sure to add [skip ci] or [ci skip], so the CI servers won't make or test another build

# Code StyleGuides

- Use the PEP 8 Standard if possible
- Use patches if possible (not needed, but if you want to, go ahead)