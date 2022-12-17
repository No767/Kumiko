# ✨ Kumiko v0.5.0 ✨

This release focuses just on major backend performances, and rewrites of the core to use Tortoise ORM instead of SQLAlchemy ORM.

## :boom: Breaking Changes :boom:

- **Dropped support for Alpine-based images and -alpine tags**. This means v0.4.x will be the last supported version to have Alpine Linux as a base. Debian 11 will now be the new base.
- **Removed unneeded -bullseye tags**. This means that the version number will be the one you want to install, and `edge` for any dev builds

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
- Include Rust (`rustc` and `cargo`) when building orjson and ormsgpack 
- Use Ormsgpack for MessagePack serialization
- Update docs (as per usual)
- Switch to using Python 3.11 for Dockerfiles, and officially support Python 3.11 for Kumiko
- Update Alpine Linux to 3.17
- Moved all checkers into tasks
- Rewrite Admin Logs to use Tortoise ORM
- Include caching with Admin Logs


## ✨ Additions

- Kumiko's custom caching library (w/ coredis)
- New delete interface for GWS inv
- MessagePack serialization for Redis
- Vagrant Support
- IPC Support with better-ipc
- Server configs
- Warn command
- Server Configs (with Server Join Handlers)

## ➖ Removals
- SQLAlchemy ORM code
- Old SQLAlchemy-based GWSs
- Old GWS Purge Inv View
- Old Library packages (GWS, Admin Logs, Eco)