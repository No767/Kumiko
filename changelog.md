# ✨ Kumiko v0.5.0 ✨

This release focuses just on major backend performances, and rewrites of the core to use Tortoise ORM instead of SQLAlchemy ORM. This update also basically fully rewrites almost all of Kumiko's core features to using Redis caching.

**Note that Kumiko will undergo major backend changes, and this release is known to be quite unstable and has not been tested. v0.6 is a full rewrite of the core backend**

## :boom: Breaking Changes :boom:

- **Dropped support for Alpine-based images and `-alpine` tags**. This means v0.4.x will be the last supported version to have Alpine Linux as a base. Debian 11 will now be the new base. See [this gist](https://gist.github.com/No767/76d87bce5e6fcb1e682d2ff932c2a6b7) for more info.
- **Removed MongoDB for Kumiko**. The new marketplace system will use PostgreSQL instead. This is done in order to correctly map relations with users, and to merge that feature into using PostgreSQL over MongoDB.
## ✨ TD;LR

- Migrate from SQLAlchemy ORM to Tortoise ORM
- Kumiko's custom caching library (w/ coredis)
- Removal of old cogs, and old code
- Unit tests

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
- Moved all checkers into tasks
- Rewrite Admin Logs to use Tortoise ORM
- Include caching with Admin Logs
- Rewrite the economy system for the 3rd time in a row
- Ensure that the DB connection is first instantiated when Kumiko starts up
- Export some Tortoise ORM models to Pydantic models for easier serialization and caching
- Use ciso8601 for parsing ISO-8601 datetimes
- Add voice support libs for Dockerfile
- Caching for Marketplace, User profile, and User Inv

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
- New caching system for Kumiko's economy using Redis
- Use aerich for migrations, and initializing db tables
- Small datetime util to help figure out whether the given datetime is a ISO-8601 datetime or not
- Reconnect/retry logic for DB connections (for PostgreSQL)
- Internal memory cache for Redis connection pools
- Full GWS rewrite
- Finally add unit tests, and code coverage
- Recursive cog loading
- ConnPool system for Redis

## ➖ Removals
- SQLAlchemy ORM code
- Old SQLAlchemy-based GWSs
- Old GWS Purge Inv View
- Old Library packages (GWS, Admin Logs, Eco)
- Old Economy V2 code
- Remove Jisho, Twitter, and MCSrvStats integration
- Auction House
- Admin Logs