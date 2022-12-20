# ✨ Kumiko v0.5.0 ✨

This release focuses just on major backend performances, and rewrites of the core to use Tortoise ORM instead of SQLAlchemy ORM.

## :boom: Breaking Changes :boom:

- **Dropped support for Alpine-based images and `-alpine` tags**. This means v0.4.x will be the last supported version to have Alpine Linux as a base. Debian 11 will now be the new base. See [this gist](https://gist.github.com/No767/76d87bce5e6fcb1e682d2ff932c2a6b7) for more info.
- **Removed MongoDB for Kumiko**. The new marketplace system will use PostgreSQL instead. This is done in order to correctly map relations with users, and to merge that feature into using PostgreSQL over MongoDB.

## ✨ TD;LR

- Migrate from SQLAlchemy ORM to Tortoise ORM
- Kumiko's custom caching library (w/ coredis)

## 🛠️ Changes
- Subclass Kumiko instead of creating the instance from `discord.Bot`
- Replace SQLAlchemy with Tortoise ORM
- Cache GWS Profiles, invs, etc
- Optimize GWS pull command
- Update Python constraints (>=3.8,<4.0)
- Upgrade PostgreSQL Dockerfile versions to 15
- Use Ormsgpack for MessagePack serialization
- Rewrite `contributing.md` and docs to further clarify topics.
- Switch to using Python 3.11 for Dockerfiles, and officially support Python 3.11 for Kumiko
- Update Alpine Linux to 3.17
- Moved all checkers into tasks
- Rewrite Admin Logs to use Tortoise ORM
- Include caching with Admin Logs
- Rewrite the economy system for the 3rd time in a row
- Ensure that the DB connection is first instantiated when Kumiko starts up
- Move IPC from bot to a dedicated cog

## ✨ Additions

- Kumiko's custom caching library (w/ coredis)
- New delete interface for GWS inv
- MessagePack serialization for Redis
- Vagrant Support
- IPC Support with better-ipc
- Server configs
- Warn command
- Server Configs (with Server Join Handlers)
- Completely rewritten economy system using Tortoise ORM, and with proper SQL and 3nf complaint relations.
- Use aerich for migrations, and initializing db tables

## ➖ Removals
- SQLAlchemy ORM code
- Old SQLAlchemy-based GWSs
- Old GWS Purge Inv View
- Old Library packages (GWS, Admin Logs, Eco)
- Old Economy V2 code
- Remove Jisho, Twitter, and MCSrvStats integration