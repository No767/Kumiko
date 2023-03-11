# ✨ Kumiko v0.6.0 ✨

This release focuses on cleaning out any old code, and getting ready for the migration to discord.py. This release is just the setup for v0.7.x, where everything is going to be re-implemented but in a more stable, and cleaner state. For more info on why, please see https://github.com/No767/Kumiko/discussions/267.

**Note that this release is considered semi-stable, but removes the whole entire economy system in preparation for a full rewrite**

## :boom: Breaking Changes :boom:

- Removed the whole entire economy system (will be re-implemented in v0.7.x) - Most of the commands will need to be re-synced globally
- Also removed GWS - Will be implemented in v0.7.x or later as a gacha system
## ✨ TD;LR

- Removed a ton of things in preparation for v0.7.x

## 🛠️ Changes
- Significant changes to the way Kumiko is built 
- Significant changes to the subclass for Kumiko
- Move IPC into a separate extension
- Rework the docs
- Merged all of Rin's cogs into one cog - Searches
- Ensure that the setup function for Redis conn pools are sync
- Cleaner recursive cog loading
- Recursive DB + Redis connections - Also uses exponential backoffs

## ✨ Additions

- New cache, utils, and economy packages (cache package uses redis-py)
- `@cached` and `@cachedJson` decorators - These will automatically cache the return value of any coroutines, and cache them on Redis
- Prisma schema
- Auto Merge Workflow for Dependabot
- Builtin global memory cache for Redis connection pools
- Datetime utils
- MsgPack support

## ➖ Removals
- The whole entire economy system
- Rin's Cogs (Merged into search feature)
- Quests (for now)
- Old packages (utils, economy, cache, etc)
- GWS (will be replaced by a gacha system in the future)
- A ton of libs
- Removed standalone setup scrips
- Removed old DB seeder scripts
- Remove of any trace of Tortoise ORM
- Tortoise ORM, Coredis, and others

# ⬆️ Dependabot Updates
- \[Actions](deps)\: Bump actions/setup-python from 4.4.0 to 4.5.0 (@dependabot)
- \[pip](deps)\: Bump python-dotenv from 0.21.1 to 1.0.0 (@dependabot)
- \[pip](deps)\: Bump asyncpraw from 7.6.1 to 7.7.0 (@dependabot)
- \[pip](deps-dev)\: Bump pre-commit from 3.1.0 to 3.1.1 (#273) (@dependabot)
- \[pip](deps)\: Bump orjson from 3.8.6 to 3.8.7 (#274) (@dependabot)
- \[pip](deps)\: Bump prisma from 0.8.1 to 0.8.2 (#276) (@dependabot)
- \[pip](deps-dev)\: Bump pytest from 7.2.1 to 7.2.2 (#277) (@dependabot)
- \[pip](deps)\: Bump charset-normalizer from 3.0.1 to 3.1.0 (#278) (@dependabot)
- \[pip](deps)\: Bump coredis from 4.10.2 to 4.10.3 (#279) (@dependabot)
- \[Actions](deps)\: Bump actions/cache from 3.2.6 to 3.3.0 (#280) (@dependabot)