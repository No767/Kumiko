# ✨ Kumiko v0.10.0 ✨

Finally Kumiko is nearly feature complete for v1. This release includes the new `pins` module, which is pretty much a tags feature. This release also includes the new Economy V4, which is the core and flagship feature of Kumiko. Ranks, jobs, and the marketplace now fully work, and more features are planned soon. On top of these, this release also fixes some bugs with the prefix and events log modules. Note that the economy feature is stable, but does have bugs and issues that folks may encounter. If there are any, please report them in the [issues](https://github.com/No767/Kumiko/issues) page on GitHub.

For the full list of changes, please see them here: [`v0.9.2...v0.10.0`](https://github.com/No767/Kumiko/compare/v0.9.2...v0.10.0)

## :boom: Breaking Changes :boom:

- There are none :smile:
## ✨ TD;LR

- Pins module (pretty much works like most tags features)
- Economy V4 (this includes the `economy`, `jobs`, and `marketplace` cogs). This feature has been the core of Kumiko, and was one of the very first features that I worked on. Now it is stable, although there are a lot of bugs and issues to fix.

## 🛠️ Changes

- Fixed bugs with the `prefix` and `events-log` cog
- Proper server config (both on PostgreSQL and Redis). The config is always cached on Redis first, and if doesn't exist, pulls from the database and reconstructs the cache entirely.
- Clarify running migrations with the docs
- Optimized Dockerfile (cut down on image size and removed unneeded things)
- Update AIOHTTP to v3.8.5 (fixes CVE-2023-37276)
- Implement file based logging support
- Upgrade Redis-Stack to 7.2.0-RC3
- Use `JSON.MERGE` instead of `JSON.SET` when replacing items in the JSON document (with Redis)

## ✨ Additions

- NSFW module (These can only be used in NSFW channels)
- Pins module
- Economy V4 (includes `economy`, `jobs`, and `marketplace` cogs).
- `is_economy_enabled` check
- Proper configuration for `eventslog` feature
- Proper SIGTERM support. Now the bot doesn't exit with an exit code 137, but now a 0.
- Implement permission check shortcuts (`is_manager`, `is_admin`, `is_mod`). Taken from RDanny because I have no time.
- Add tasks to update pay and restock items. Done per hour
- Add local `eco_user` table 

## ➖ Removals
- Old "community docs"
- Old scripts

# ⬆️ Dependabot Updates

- \[pip](deps)\: Bump asyncpraw from 7.7.0 to 7.7.1 (#378) (@dependabot)
- \[pip](deps-dev)\: Bump pyright from 1.1.316 to 1.1.317 (#379) (@dependabot)
- \[pip](deps-dev)\: Bump ruff from 0.0.277 to 0.0.278 (#381) (@dependabot)
- \[pip](deps-dev)\: Bump pytest-asyncio from 0.21.0 to 0.21.1 (#380) (@dependabot)
- \[Actions](deps)\: Bump actions/setup-python from 4.6.1 to 4.7.0 (#382) (@dependabot)
- \[pip](deps-dev)\: Bump pyright from 1.1.317 to 1.1.318 (#387) (@dependabot)
- \[pip](deps-dev)\: Bump pyinstrument from 4.5.0 to 4.5.1 (#388) (@dependabot)
- \[pip](deps-dev)\: Bump ruff from 0.0.278 to 0.0.280 (#389) (@dependabot)