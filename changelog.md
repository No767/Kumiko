# ✨ Kumiko v0.7.0 ✨

This release is the foundation for v0.8.x. This release implements almost everything back (excluding the advanced moderation features, and economy system) from previous versions of Kumiko, and now Kumiko is migrated to Discord.py (sorry Pycord devs). The economy system and improved moderation commands will be coming in v0.8.x instead. There might be some that might have been missed, so if you want to see the full list of changes, please see the changes here: [`v0.6.0...v0.7.x`](https://github.com/No767/Kumiko/compare/v0.6.0...v0.7.0)

## :boom: Breaking Changes :boom:

- Literally rewrote Kumiko from the ground up to use Discord.py instead of Pycord. Expect a ton of things to be broken
- A ton of cogs, and commands have been either moved or deleted since v0.6.x. Please consider resyncing your commands with the include dev-tool cog (or by activating jishaku)

## ✨ TD;LR

- Migrated from Pycord to Discord.py. Literally this took way too long
- Kumiko now supports both prefixed and slash commands (default prefix is `>`)
- Migration from Coredis to Redis-py, and migration from Tortoise ORM to Prisma
- Kumiko is now properly type hinted/statically typed now.

## 🛠️ Changes
- RedisCheck is now fully recursive
- Properly implemented static type checking
- Improved DB connections via DB cog
- Migrate searches cog to dpy
- Spilt Reddit and GitHub commands to their respective cogs
- Use `@app_commands.describe` to describe the slash command inputs. Removed the docstring args bc it was conflicting w/ the help cmd
- Now using a singleton object for storing Redis connection pools. (Known as the KumikoCPM)
- Improved the Vagrantfile (possible Ansible provisioning in the future)
- Using orjson for parsing JSON instead of pysimdjson or cysimdjson

## ✨ Additions
- Context manager for Prisma sessions - Useful for debugging and testing
- Recursive RedisCheck coroutine - Actually now cleans up the stack calls for once (thanks to a base case)
- Vasic help command - Will be improved in v0.8.x
- New unit tests
- Pagination - Taken from Rapptz's (Danny) RoboDanny bot, and improved to work w/ Kumiko
- EmbedListSource for paginating embeds
- TextSources, and ListSources for paginating text and lists
- Actions cog - Replacement for the UwU Cog
- Error Handler cog - Now uses custom exceptions
- exceptions and utils (including datetime parsing utils, and much much more)
- Dev Mode - It's an environment variable that toggles the dev mode. This is useful for testing, and debugging Kumiko (includes Jishaku and a custom extension reloader)


## ➖ Removals
- MsgPack Serialization
- Literally all of the cogs from v0.6.x
- Removed python-dateutil, numpy, pytimeparse, aiocache, ormsgpack, and pysimdjson (yay no C compilations anymore) 
- Old libs
- Pycord itself
- Builtlins cache in favor of KumikoCPM

# ⬆️ Dependabot Updates
- \[Actions](deps)\: Bump actions/cache from 3.3.0 to 3.3.1 (#282) (@dependabot)
- \[pip](deps-dev)\: Bump pyright from 1.1.298 to 1.1.299 (#283) (@dependabot)
- \[pip](deps-dev)\: Bump pre-commit from 3.1.1 to 3.2.0 (#284) (@dependabot)
- \[pip](deps)\: Bump redis from 4.5.1 to 4.5.2 (#285) (@dependabot)
- \[pip](deps-dev)\: Bump pytest-asyncio from 0.20.3 to 0.21.0 (#286) (@\dependabot)
- \[pip](deps)\: Bump orjson from 3.8.7 to 3.8.8 (#288) (@dependabot)
- \[pip](deps-dev)\: Bump pyright from 1.1.299 to 1.1.300 (#289) (@dependabot)
- \[pip](deps)\: Bump redis from 4.5.2 to 4.5.3 (#290) (@dependabot)
- \[pip](deps-dev)\: Bump pre-commit from 3.2.0 to 3.2.1 (#291) (@dependabot)
- \[pip](deps)\: Bump orjson from 3.8.8 to 3.8.9 (#293) (@dependabot)
- \[pip](deps-dev)\: Bump pyright from 1.1.300 to 1.1.301 (#294) (@dependabot)
- \[pip](deps)\: Bump redis from 4.5.3 to 4.5.4 (#295) (@dependabot)
