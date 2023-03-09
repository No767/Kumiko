# ✨ Kumiko v0.6.0 ✨

This release focuses on cleaning out any old code, and getting ready for the migration to discord.py. This release is just the setup for v0.7.x, where everything is going to be re-implemented but in a more stable, and cleaner state. For more info on why, please see https://github.com/No767/Kumiko/discussions/267.

**Note that this release is considered semi-stable, but removes the whole entire economy system in preparation for a full rewrite**

## :boom: Breaking Changes :boom:

- Removed the whole entire economy system (will be re-implemented in v0.7.x) - Most of the commands will need to be re-synced globally

## ✨ TD;LR

- Removed a ton of things in preparation for v0.7.x

## 🛠️ Changes
- Significant changes to the way Kumiko is built 
- Significant changes to the subclass for Kumiko
- Move IPC into a separate extension
- Rework the docs


## ✨ Additions

- New cache, utils, and economy packages
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