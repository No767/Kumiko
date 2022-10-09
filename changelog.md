# ✨ Kumiko v0.4.0 ✨

This update brings a ton of new things, and a complete overhaul from what things used to be in `v0.3.0`. With this update, we have reached over 2000 commits for Kumiko, and merges all commits from upstream Rin v2.2.x. With a stable codebase for the economy system, tons of new features and critical improvements, Kumiko has never been better. In fact, this release of Kumiko fixes almost everything that `v0.3.0` had wrong. For details for upstream changes from Rin, please refer to the links below (latest point release):

- Rin v2.2.7: https://github.com/No767/Rin/releases/tag/v2.2.7

## ✨ TD;LR

A ton of new features, including:

- Kumiko's Quests System
- Genshin-based Wish Sim (GWS)
- Kumiko's Auction House
- Basic Admin Commands
- Admin Logs System

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
- Completely redid Help command
- Organize Cogs into different directories determined by if the cogs came from Rin or Kumiko
- Display what bot user is being logged into
- Merged all PostgreSQL DBs into one (instead of having them separated)
- Updated `ws_data.sql` and `ws_data.csv` files


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
- New Help Command
- `POSTGRES_KUMIKO_DB` env var for `start.sh`

## ➖ Removals

- Deprecated code using SQLAlchemy Core instead of SQLAlchemy ORM
- DeviantArt Cog (from Rin)
- More old libs
- QRCode Maker Cog
- GWS Banner Commands
- Arch + Ubuntu Dockerfile
- `kumikoinfo.py` Cog
- `kumikoping.py` Cog
- `kumiko-platform.py` Cog
- Unload `advice.py`, `blue-alliance.py`, `discord-bots.py`, `first-frc-events.py`, `hypixel.py`, `spiget.py`, `top-gg.py`, and `twitch.py` Cogs (this is due to the new help system only allowing up to 25 options, and therefore only 25 categories can be shown)
- Remove `BLUE_ALLIANCE_API_KEY`, `DISCORD_BOTS_API_KEY`, `FIRST_EVENTS_FINAL_KEY`, `HYPIXEL_API_KEY`,  `TOP_GG_API_KEY`, `TWITCH_API_ACCESS_TOKEN`, `TWITCH_API_CLIENT_ID` env vars from `start.sh` and `.env-docker-example`
- Remove `POSTGRES_ECO_USERS_DB`, `POSTGRES_WS_DB`, `POSTGRES_AH_DB`, `POSTGRES_QUESTS_DB`, and `POSTGRES_AL_DB` env vars from `start.sh` and `.env-docker-example`


## ⬆️ Dependency Updates

- \[Actions](deps)\: Bump actions/cache from 3.0.5 to 3.0.6 (@dependabot[bot])
- \[pip](deps)\: Bump sqlalchemy from 1.4.39 to 1.4.40 (@dependabot[bot])
- \[Actions](deps)\: Bump actions/cache from 3.0.6 to 3.0.7 (@dependabot[bot])
- \[pip](deps)\: Bump aiormq from 6.4.0 to 6.4.1 (@dependabot[bot])
- \[pip](deps)\: Bump rin-exceptions from 1.0.2 to 1.0.3 (@dependabot[bot])
- \[pip](deps)\: Bump numpy from 1.23.1 to 1.23.2 (@dependabot[bot])
- \[pip](deps)\: Bump orjson from 3.7.11 to 3.7.12 (@dependabot[bot])
- \[pip](deps)\: Bump orjson from 3.7.11 to 3.7.12 (@dependabot[bot])
- \[pip](deps)\: Bump rin-exceptions from 1.0.2 to 1.0.3 (@dependabot[bot])
- \[pip](deps)\: Bump py-cord from 2.0.0 to 2.0.1 (@dependabot[bot])
- \[pip](deps)\: Bump py-cord from 2.0.0 to 2.0.1 (@dependabot[bot])
- \[pip](deps)\: Bump beanie from 1.11.7 to 1.11.8 (@dependabot[bot])
- \[pip](deps)\: Bump beanie from 1.11.8 to 1.11.9 (@dependabot[bot])
- \[Actions](deps)\: Bump actions/cache from 3.0.7 to 3.0.8 (@dependabot[bot])
- \[pip](deps-dev)\: Bump pyinstrument from 4.2.0 to 4.3.0 (@dependabot[bot])
- \[pip](deps)\: Bump py-cord from 2.0.1 to 2.1.0 (@dependabot[bot])
- \[pip](deps)\: Bump py-cord from 2.0.1 to 2.1.1 (@dependabot[bot])
- \[pip](deps)\: Bump py-cord from 2.1.0 to 2.1.1 (@dependabot[bot])
- \[pip](deps)\: Bump orjson from 3.7.12 to 3.8.0 (@dependabot[bot])
- \[pip](deps)\: Bump orjson from 3.7.12 to 3.8.0 (@dependabot[bot])
- \[pip](deps)\: Bump python-dotenv from 0.20.0 to 0.21.0 (@dependabot[bot])
- \[pip](deps)\: Bump python-dotenv from 0.20.0 to 0.21.0 (@dependabot[bot])
- \[Actions](deps)\: Bump actions/checkout from 2 to 3 (@dependabot[bot])
- \[Actions](deps)\: Bump actions/cache from 2 to 3 (@dependabot[bot])
- \[pip](deps)\: Bump py-cord from 2.1.1 to 2.1.2 (@dependabot[bot])
- \[pip](deps)\: Bump py-cord from 2.1.2 to 2.1.3 (@dependabot[bot])
- \[pip](deps)\: Bump py-cord from 2.1.1 to 2.1.3 (@dependabot[bot])
- \[pip](deps)\: Bump sqlalchemy from 1.4.40 to 1.4.41 (@dependabot[bot])
- \[Actions](deps)\: Bump actions/checkout from 2 to 3 (@dependabot[bot])
- \[Actions](deps)\: Bump actions/checkout from 2 to 3 (@dependabot[bot])
- \[pip](deps)\: Bump numpy from 1.23.2 to 1.23.3 (@dependabot[bot])
- \[pip](deps)\: Bump numpy from 1.23.2 to 1.23.3 (@dependabot[bot])
- \[pip](deps)\: Bump pysimdjson from 5.0.1 to 5.0.2 (@dependabot[bot])
- \[pip](deps)\: Bump pysimdjson from 5.0.1 to 5.0.2 (@dependabot[bot])
- \[pip](deps)\: Bump aiormq from 6.4.1 to 6.4.2 (@dependabot[bot])
- \[pip](deps)\: Bump uvloop from 0.16.0 to 0.17.0 (@dependabot[bot])
- \[pip](deps)\: Bump uvloop from 0.16.0 to 0.17.0 (@dependabot[bot])
- \[pip](deps)\: Bump beanie from 1.11.9 to 1.11.10 (@dependabot[bot])
- \[Actions](deps)\: Bump actions/setup-node from 3.4.1 to 3.5.0 (@dependabot[bot])
- \[pip](deps)\: Bump beanie from 1.11.10 to 1.11.11 (@dependabot[bot])
- \[pip](deps-dev)\: Bump mypy from 0.971 to 0.981 (@dependabot[bot])
- \[pip](deps)\: Bump beanie from 1.11.11 to 1.11.12 (@dependabot[bot])
- \[Actions](deps)\: Bump actions/cache from 3.0.8 to 3.0.9 (@dependabot[bot])
- \[pip](deps)\: Bump py-cord from 2.1.3 to 2.2.0 (@dependabot[bot])
- \[Actions](deps)\: Bump actions/cache from 3.0.9 to 3.0.10 (@dependabot[bot])
- \[pip](deps-dev)\: Bump mypy from 0.981 to 0.982 (@dependabot[bot])
- \[pip](deps)\: Bump py-cord from 2.2.0 to 2.2.2 (@dependabot[bot])
- \[pip](deps)\: Bump beanie from 1.11.12 to 1.12.0 (@dependabot[bot])