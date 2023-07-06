# ✨ Kumiko v0.9.0 ✨

More reworks of literally everything... This release migrates from Prisma to pure SQL (asyncpg), and fully stabilities the repo to use discord.py instead of Pycord. Nearly all of the planned features are implemented in this release, except the economy module.
For the full list of changes, please see them here: [`v0.8.x...v0.9.0`](https://github.com/No767/Kumiko/compare/v0.8.0...v0.9.0)

## :boom: Breaking Changes :boom:

- All of the SQL queries have been rewritten to use SQL w/ asyncpg instead of Prisma
- A ton of cogs, and commands have been either moved or deleted since v0.8.x. Please consider resyncing your commands with the include dev-tool cog (or by activating jishaku)

## ✨ TD;LR

- Migration from Prisma to asyncpg
- Kumiko now supports custom prefixes (max is 10). The default that will be set is `>`
- asyncpg-trek migration system
- Kumiko's EventsLog module has been implemented
- Docs has been merged into one repo (https://kumiko.readthedocs.io/en/latest/index.html)

## 🛠️ Changes
- Allow actions commands to greedily consume users to mention
- Replaced RedisCheck with an simple ping check (`ensureOpenRedisConn`)
- Replace all Prisma related code with asyncpg code
- Reuse AIOHTTP `ClientSession`, `asyncpg.Pool`, `redis.asyncio.connection.ConnectionPool`, and `LRU` objects throughout the lifecycle of the bot
- Hide `.python-version` file from the repo
- Expect `id` and `redis_pool` args to be in an function when using `@cache` or `@cacheJson` decos
- Update docs to add new instructions for hosting, and new requirements
- Don't stack context managers, but rather spawn 3 new ones in one go (this is recommended instead)
- Update Dockerfile to use Debian 12 (Bookworm)
- Use `Embed.timestamp` for some embeds to show timestamps
- Replaced `.gitignore` with a proper one from GitHub
- Replaced `kumiko.py` with `meta.py` to allow for clearer purpose


## ✨ Additions
- Migrations system using asyncpg-trek
- SQL migrations
- SQL based code to replace Prisma
- Context manager based logging system
- Custom prefix module (aka Kumiko supports custom prefixes for guilds)
- Ansible playbooks, proper Vagrant config
- Discord API events handler, custom dispatch events
- Prefix utils
- EventsLog module
- Ping checks to ensure that the connections are open for PostgreSQL and Redis
- Docs merged into one repo - this repo
- Added `display_emoji` property to allow for cogs to have emojis when being loaded in the select menus
- The final version of what an help command should be (taken from RDanny directly as usual)

## ➖ Removals
- Global KumikoCPM variable in favor of having it stored during runtime instead
- Old economy packages
- cog-ext module
- Prisma along with other unused libs

# ⬆️ Dependabot Updates
- \[pip](deps-dev)\: Bump pre-commit from 3.2.1 to 3.2.2 (#300) (@dependabot)
- \[pip](deps-dev)\: Bump pyright from 1.1.301 to 1.1.302 (#301) (@dependabot)
- \[pip](deps-dev)\: Bump pytest from 7.2.2 to 7.3.0 (#302) (@dependabot)
- \[pip](deps)\: Bump orjson from 3.8.9 to 3.8.10 (#303) (@dependabot)
- \[pip](deps-dev)\: Bump pytest from 7.3.0 to 7.3.1 (#304) (@dependabot)
- \[pip](deps-dev)\: Bump pyright from 1.1.302 to 1.1.303 (#305) (@dependabot)
- \[pip](deps-dev)\: Bump ruff from 0.0.261 to 0.0.262 (#306) (@dependabot)
- \[Actions](deps)\: Bump actions/setup-python from 4.5.0 to 4.6.0 (#307) (@dependabot)
- \[pip](deps-dev)\: Bump pyright from 1.1.303 to 1.1.304 (#308) (@dependabot)
- \[pip](deps-dev)\: Bump sphinx from 6.1.3 to 6.2.0 (#310) (@dependabot)
- \[pip](deps-dev)\: Bump nox from 2022.11.21 to 2023.4.22 (@dependabot)
- \[pip](deps-dev)\: Bump sphinx from 6.2.0 to 6.2.1 (#312) (@dependabot)
- \[pip](deps-dev)\: Bump ruff from 0.0.262 to 0.0.263 (#313) (@dependabot)
- \[pip](deps-dev)\: Bump pyright from 1.1.304 to 1.1.305 (#314) (@dependabot)
- \[pip](deps)\: Bump orjson from 3.8.10 to 3.8.11 (#315) (@dependabot)
- \[pip](deps)\: Bump discord-py from 2.2.2 to 2.2.3 (#316) (@dependabot)
- \[pip](deps-dev)\: Bump pre-commit from 3.2.2 to 3.3.0 (#317) (@dependabot)
- \[pip](deps-dev)\: Bump pre-commit from 3.3.0 to 3.3.1 (#318) (@dependabot)
- \[pip](deps-dev)\: Bump ruff from 0.0.263 to 0.0.264 (#319) (@dependabot)
- \[pip](deps-dev)\: Bump pyright from 1.1.305 to 1.1.306 (#320) (@dependabot)
- \[pip](deps-dev)\: Bump ruff from 0.0.264 to 0.0.265 (#321) (@dependabot)
- \[pip](deps)\: Bump orjson from 3.8.11 to 3.8.12 (#322) (@dependabot)
- \[pip](deps)\: Bump redis from 4.5.4 to 4.5.5 (#324) (@dependabot)
- \[pip](deps)\: Bump gql from 3.4.0 to 3.4.1 (#323) (@dependabot)
- \[pip](deps-dev)\: Bump pyright from 1.1.306 to 1.1.307 (#325) (@dependabot)
- \[pip](deps-dev)\: Bump pyright from 1.1.307 to 1.1.308 (#326) (@dependabot)
- \[pip](deps-dev)\: Bump ruff from 0.0.265 to 0.0.267 (#327) (@dependabot)
- \[pip](deps-dev)\: Bump pyright from 1.1.308 to 1.1.309 (#328) (@dependabot)
- \[pip](deps-dev)\: Bump pre-commit from 3.3.1 to 3.3.2 (#329) (@dependabot)
- \[pip](deps-dev)\: Bump ruff from 0.0.267 to 0.0.269 (#330) (@dependabot)
- \[pip](deps-dev)\: Bump furo from 2023.3.27 to 2023.5.20 (#331) (@dependabot)
- \[pip](security)\: Bump requests from 2.28.2 to 2.31.0 (#332) (@dependabot)
- \[Actions](deps)\: Bump actions/setup-python from 4.6.0 to 4.6.1 (#333) (@dependabot)
- \[pip](deps)\: Bump orjson from 3.8.12 to 3.8.13 (#334) (@dependabot)
- \[pip](security)\: Bump tornado from 6.2 to 6.3.2 (#336) (@dependabot)
- \[pip](deps-dev)\: Bump pyright from 1.1.309 to 1.1.310 (#337) (@dependabot)
- \[pip](deps-dev)\: Bump pytest-cov from 4.0.0 to 4.1.0 (#335) (@dependabot)
- \[pip](deps-dev)\: Bump ruff from 0.0.269 to 0.0.270 (#338) (@dependabot)
- \[pip](deps)\: Bump orjson from 3.8.13 to 3.8.14 (#339) (@dependabot)
- \[pip](deps-dev)\: Bump pyright from 1.1.310 to 1.1.311 (#340) (@dependabot)
- \[pip](deps)\: Bump orjson from 3.8.14 to 3.9.0 (#341) (@dependabot)
- \[pip](deps-dev)\: Bump pyinstrument from 4.4.0 to 4.5.0 (#342) (@dependabot)
- \[pip](deps-dev)\: Bump ruff from 0.0.270 to 0.0.271 (#343) (@dependabot)
- \[pip](deps-dev)\: Bump pyright from 1.1.311 to 1.1.313 (#344) (@dependabot)
- \[pip](deps-dev)\: Bump ruff from 0.0.271 to 0.0.272 (#345) (@dependabot)
- \[Actions](deps)\: Bump docker/build-push-action from 4.0.0 to 4.1.0 (#346) (@dependabot)
- \[pip](deps)\: Bump orjson from 3.9.0 to 3.9.1 (#347) (@dependabot)
- \[pip](deps-dev)\: Bump pytest from 7.3.1 to 7.3.2 (#348) (@dependabot)
- \[pip](deps)\: Bump prisma from 0.8.2 to 0.9.0 (#349) (@dependabot)
- \[pip](deps)\: Bump discord-py from 2.2.3 to 2.3.0 (#350) (@dependabot)
- \[Actions](deps)\: Bump docker/build-push-action from 4.1.0 to 4.1.1 (#352) (@dependabot)
- \[pip](deps-dev)\: Bump myst-parser from 1.0.0 to 2.0.0 (@dependabot)
- \[pip](deps-dev)\: Bump pre-commit from 3.3.2 to 3.3.3 (#354) (@dependabot)
- \[pip](deps-dev)\: Bump pyright from 1.1.313 to 1.1.314 (#356) (@dependabot)
- \[pip](deps-dev)\: Bump sphinx from 6.2.1 to 7.0.1 (@dependabot)
- \[pip](deps-dev)\: Bump pyright from 1.1.314 to 1.1.315 (#357) (@dependabot)
- \[pip](deps-dev)\: Bump ruff from 0.0.272 to 0.0.274 (#358) (@dependabot)
- \[pip](deps-dev)\: Bump ruff from 0.0.274 to 0.0.275 (#359) (@dependabot)
- \[pip](deps-dev)\: Bump pytest from 7.3.2 to 7.4.0 (#360) (@dependabot)
- \[pip](deps)\: Bump discord-py from 2.3.0 to 2.3.1 (#361) (@dependabot)
- \[pip](deps)\: Bump redis from 4.5.5 to 4.6.0 (#363) (@dependabot)
- \[pip](deps-dev)\: Bump pyright from 1.1.315 to 1.1.316 (#362) (@dependabot)
- \[pip](deps)\: Bump prisma from 0.9.0 to 0.9.1 (#367) (@dependabot)
- \[pip](deps-dev)\: Bump ruff from 0.0.275 to 0.0.276 (#370) (@dependabot)
- \[pip](deps-dev)\: Bump ruff from 0.0.276 to 0.0.277 (#371) (@dependabot)
- \[Actions](deps)\: Bump actions/setup-node from 3.6.0 to 3.7.0 (#372) (@dependabot)