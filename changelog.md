# ✨ Kumiko v0.3.0 ✨

This update focuses on Kumiko's Economy system (which was completely rebuilt from the ground up), and upstream commits from Rin v1.4.x, v2.0.x, v2.1.x and dev branch. This update together is probably literally 500+ commits more than Kumiko v0.2.0. For details for upstream changes from Rin, please refer to the following links (latest point releases):

- Rin v1.4.4: https://github.com/No767/Rin/releases/tag/v1.4.4
- Rin v2.0.2: https://github.com/No767/Rin/releases/tag/v2.0.2
- Rin v2.1.0: https://github.com/No767/Rin/releases/tag/v2.1.0

## TD;LR

- Rebuilt Kumiko's Economy system from the ground up
- All upstream commits from Rin v1.4.x, v2.0.x, v2.1.x and dev branch
- Migrate all commands to slash commands

## Changes

- Rebuilt Kumiko's Economy system from the ground up.
- Switch to using Rin-Exceptions package from PyPi
- Use PM2 for process management (from upstream Rin)
- Require all new items being stored to contain an UUID
- Finished user inv + transaction system
- Full proper exception handling for all commands (including eco commands)
- Search User's ID for Inv Method instead
- Organize eco commands into groups
- Include User signup
- Attempt to redo ban + pronoun cogs
- Use pre-commit hooks instead of format workflow
- Upgrade all Python versions in workflows to 3.10.5
- Make sure that the fields for the user inv are correct and set
- Moved User inv from MongoDB to PostgreSQL

## Additions
- The full rebuild of the economy system
- economy_utils package (used by the economy system)
- Beg command
- Add Task template on GitHub Issues
- Add timeouts to eco-init buttons
- Add user transaction command
- Add command to search via UUID
- Include commands to be able to add items, and remove items from the marketplace
- Add platform cog
- Proper docstrings for all economy_utils coroutines
- Add Regex filters when creating marketplace items

## Removals

- Chat, Global, DisQuest, and many many other cogs
- All of the old patches (never worked anyways)
- Old economy files
- Exceptions package (use Rin-Exceptions package from PyPi instead)
- Format workflow
- Arch-Docker Dockerfile
- Removed Unused and unneeded coroutines