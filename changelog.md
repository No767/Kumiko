# ✨ Kumiko v0.4.0 ✨

This update brings a ton of new things, and a complete overhaul from what things used to be in `v0.3.0`. With this update, we have reached over 2000 commits for Kumiko, and merges all commits from upstream Rin v2.2.x. With a stable codebase for the economy system, tons of new features and critical improvements, Kumiko has never been better. In fact, this release of Kumiko fixes almost everything that `v0.3.0` had wrong. For details for upstream changes from Rin, please refer to the links below (latest point release):

- Rin v2.2.7: https://github.com/No767/Rin/releases/tag/v2.2.7
## ✨ TD;LR

A ton of new features, including:

- Kumiko's Quests System
- Genshin-based Wish Sim (GWS)
- Kumiko's Auction House
- Basic Admin Commands

And some backend changes w/ Docker support:

- Switch to a Dockerfile system based off of `tini` and `alpine` instead of PM2 (Credits for @TheSilkky for developing the Alpine Dockerfile)
- Deploy both Alpine and Debian-based Dockerfiles
- Automatic DB schema creator (called the "seeder")
- Improved Docker Compose support + Standalone support

## 🔥 Breaking Changes

- **Switched from Pipenv to Poetry**
- **Remove support for prefixed commands**
- **Remove legacy help cog**

## 🛠️ Changes

- Swap from SQLAlchemy Core to SQLAlchemy ORM
- Rename the currency from coins to Lavender Petals
- Standardize all datetime as ISO-8601 for all timestamps
- Charge initial fee for selling items on the marketplace 
- Audit all service commands from Rin
- Require all DB Coroutines to include URI argument for URI Connection Strings
- Migrate from Env Variables to URI Connection Strings for Marketplace
- Allow for ext envs to be passed through for Docker deployment
- Fix Postgres-Init script (#144)
- Include improvements for Reddit + Waifu cog from Reina
- Use `discord.Member` for avatar cmds inputs instead of using `str`
- Make Debian now the latest `edge` tag
- Require input type to be `discord.Member` instead of `str` in UwU cog
- Swap from `github.repository_owner` to `github.actor` to fix GHCR build workflows
- Bump Python version to 3.10.7 for Alpine and Debian Dockerfiles
- Display Pycord version w/ bot info command
- Optimize Dynamic Cog Loader
- Update Docs
- Don't `echo` database schema creations w/ SQLAlchemy
- Improved Docker Compose setup (literally just download some stuff, set up the env file, and run)
- Append `eco` to all economy commands
- Unload RabbitMQ consumer for Kumiko
- Provide a general exception embed for admin commands


## ✨ Additions
- Kumiko's Quests System
- Genshin-based Wish Sim (GWS)
- Kumiko's Auction House (Uses Redis + RabbitMQ)
- Docker Compose Example + ENV Examples
- Docker Compose Support
- Alpine + Debian Dockerfiles w/ `tini` for running Kumiko
- RabbitMQ Consumer Cog
- Redis for selecting and caching
- RabbitMQ for auction house message queues
- Basic Admin Commands
- UwU Commands
- Avatar fetcher commands (#109)
- AH Checker + Quests Checker Cogs
- Add marketplace listing cooldowns
- Basic info commands
- Use Dynamic Cog Loader instead of loading cogs from a list
- Add new self-host guide
- Automatic DB schema creator (called the "seeder")
- Database init scripts for Docker Compose 
- `setup.sh` and `standalone-setup.sh` for both Docker Compose setups and standalone setups
- `wait-for` script within Docker Compose (to wait until PostgreSQL and RabbitMQ start accepting connections)
- Custom PostgreSQL docker image for Docker Compose
- Admin Logs

## ➖ Removals

- Deprecated code using SQLAlchemy Core instead of SQLAlchemy ORM
- DeviantArt Cog (from Rin)
- More old libs
- QRCode Maker Cog
- GWS Banner Commands
- Arch + Ubuntu Dockerfile