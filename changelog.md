# ✨ Kumiko v0.11.0 ✨

The final feature release before bugfixing and staging tests begin. This release includes changes such as the introduction of the auction house, pronouns module, and others. These features are considered to be stable but will contain bugs and issues. Please report any bugs you find to the [issue tracker](https://github.com/No767/Kumiko/issues) if you find one.

For the full list of changes, please see them here: [`v0.10.2...v0.11.0`](https://github.com/No767/Kumiko/compare/v0.10.2...v0.11.0)

> As a side note, I (Noelle) will not be working on Kumiko as actively as before due to college and work so releases will not be as frequent as before.

## :boom: Breaking Changes :boom:

- There are none :smile:

## ✨ TD;LR

- Implement the Auction House module (#390)
- Implement the Redirects module
- Kumiko is fully up to PEP8 standards

## 🛠️ Changes

- Use discord.py styled versioning schema
- Use RoboDanny styled uptime tracker
- Optimize error handler stack
- Support systemd journal handlers
- Use msgspec as a replacement to attrs and faster serialization/deserialization
- Upgrade redis stack to 7.2.0-RC3
- Use SonarCloud to enforce code quality
- Move connection checks into one file
- Use `verify-full` for SSL PostgreSQL connections
- Condense Reddit cog
- Start tasks in `cog_load` instead of constructor
- Ensure that the codebase is linted through better Pyright and Ruff configs
- Use grouped unique keys to enforce M-M relations
- Update docs to reflect PEP8 standards
- Improved traceback formatting for backwards compatibility
- Use `msgspec.Struct` instead of `attrs` for faster serializations
- Improve Redis caching
- Improve event logs by using better redis caching and structs instead
- Provide more fixes to the jobs module


## ✨ Additions

- Implement message constants enums
- Use SonarCloud to enforce code quality
- Implement Auction House, refund, and pronouns commands
- Add buttons within inventory in order to access AH easier
- Systemd journal handler
- Leaderboard command
- Implement dictionary module (supports both English and Japanese)
- Implement a purchase command for the Auctions module
- More test coverage
- Implement the Redirects module (allows you to redirect overlapping conversations into threads)
- Implement the `resolved` command to mark a thread as resolved. Also works on fourms
- Add `FUNDING.yml` (because I am a broke college student and I need money)
- Simple healthcheck ipc endpoint


## ➖ Removals

- Old help command
- Dead code / commented out code
- Unused tables and indexes (the m-m tables got dropped)


# ⬆️ Dependabot Updates

- \[pip](deps-dev)\: Bump sphinx from 7.0.1 to 7.1.0 (#394) (@dependabot)
- \[pip](deps-dev)\: Bump furo from 2023.5.20 to 2023.7.26 (#397) (@dependabot)
- \[pip](deps-dev)\: Bump sphinx from 7.1.0 to 7.1.1 (#398) (@dependabot)
- \[pip](deps-dev)\: Bump ruff from 0.0.280 to 0.0.282 (#399) (@dependabot)
- \[pip](deps-dev)\: Bump sphinx from 7.1.1 to 7.1.2 (#402) (@dependabot)
- \[pip](deps-dev)\: Bump pyright from 1.1.318 to 1.1.320 (#403) (@dependabot)
- \[pip](deps)\: Bump orjson from 3.9.2 to 3.9.3 (#404) (@dependabot)
- \[pip](deps)\: Bump orjson from 3.9.3 to 3.9.4 (#405) (@dependabot)
- \[pip](deps-dev)\: Bump ruff from 0.0.282 to 0.0.283 (#406) (@dependabot)
- \[pip](deps)\: Bump faust-cchardet from 2.1.18 to 2.1.19 (#407) (@dependabot)
- \[pip](deps-dev)\: Bump ruff from 0.0.283 to 0.0.284 (#408) (@dependabot)
- \[pip](deps-dev)\: Bump pyright from 1.1.320 to 1.1.321 (#409) (@dependabot)
- \[pip](deps)\: Bump msgspec from 0.17.0 to 0.18.0 (#410) (@dependabot)
- \[pip](deps)\: Bump discord-py from 2.3.1 to 2.3.2 (#411) (@dependabot)
- \[pip](deps-dev)\: Bump pyright from 1.1.321 to 1.1.322 (#414) (@dependabot)
- \[Actions](deps)\: Bump actions/setup-node from 3.7.0 to 3.8.0 (#415) (@dependabot)