# ✨ Rin V2.2.0 (LTS) ✨

**This will be the last version of Rin to contain new features. Rin v2.2.0 is considered an LTS release, and will be supported for the next 3-6 months from the release date. Within the next patch versions, slight changes and modifications will be made to Rin. For more info, please see the gist linked [here](https://gist.github.com/No767/de27c61dc471ac331a45ea7c2bda62c0)**

This update brings in a ton of changes, including swapping to paginators instead, a new Dockerfile + Docker build system, and generally a ton of improvements. This version is meant to replace the v2.0.3.x versions used in production.

## Changes
- Swap to completely using paginators instead of just spamming with embeds
- Completely audit all 65-70+ service commands
- Completely audit all non-service cogs and commands
- Replace Twitter Search with Twitter API v2
- Removed all commands that required ID input
- Switch to using Rin-Exceptions package
- Upgraded Tenor Service to API v2
- Return Original URL for that item in service cogs (if applicable)
- Updated some command names
- Bump Alpine Python version to 3.10.6
- Bump supported Python version to 3.10.6
- Bump GitPod default python version to 3.10.6
- Defer Docker Build workflows by 60 seconds (to allow for tagging to happen first)
- Update Help command with the latest commands
- Use an more efficient way to load all cogs
- Changed activity from `Watching /rinhelp` to `Watching /help` 
- Also log when Rin is fully ready
- Prevent GitPod from making Pre-Builds for PRs
- Bump Python Version on Workflows to the latest version of 3.10

## Additions

- Alpine-based Dockerfile + Start.sh (allowing Rin to be deployed anywhere and self-hosted. Thanks Ellie. (@TheSilkky))  
- Docker Build + Deploy Workflow for GHCR + Docker Hub (Thanks Ellie. (@TheSilkky))
- Twitch API Support
- Waifu.IM API Support
- Logging for Rin
- Docker Compose Support
- Environment variable for testing discord bot on dev docker builds

## Removals
- Removed all commands that required ID input
- MyWaifuList Support
- Removed DeviantArt API Support
- QRCode Maker Cog
- Any old libs
- Rinhelp command (replaced by a standard `/help` command)

## Dependency Updates
- \[pip](deps)\: Bump orjson from 3.7.2 to 3.7.3 (@dependabot)
- \[pip](deps)\: Bump sqlalchemy from 1.4.37 to 1.4.38 (@dependabot)
- \[pip](deps)\: Bump orjson from 3.7.3 to 3.7.5 (@dependabot)
- \[pip](deps)\: Bump lxml from 4.9.0 to 4.9.1 (@dependabot)
- \[pip](deps)\: Bump orjson from 3.7.5 to 3.7.6 (@dependabot)
- \[pip](deps)\: Bump rin-exceptions from 1.0.0 to 1.0.1 (@dependabot)
- \[pip](deps)\: Bump ujson from 5.3.0 to 5.4.0 (@dependabot)
- \[pip](deps)\: Bump asyncpg from 0.25.0 to 0.26.0 (@dependabot)
- \[pip](deps)\: Bump orjson from 3.7.6 to 3.7.7 (@dependabot)
- \[Actions](deps)\: Bump actions/setup-node from 3.3.0 to 3.4.0 (@dependabot)
- \[pip](deps)\: Bump py-cord from 2.0.0rc1 to 2.0.0 (@dependabot)
- \[pip](deps-dev)\: Bump pre-commit from 2.19.0 to 2.20.0 (@dependabot)
- \[Actions](deps)\: Bump actions/setup-node from 3.4.0 to 3.4.1 (@dependabot)
- \[pip](deps)\: Bump gql from 3.3.0 to 3.4.0 (@dependabot)
- \[pip](deps)\: Bump rin-exceptions from 1.0.1 to 1.0.2 (@dependabot)
- \[pip](deps)\: Bump orjson from 3.7.7 to 3.7.8 (@dependabot)
- \[Actions](deps)\: Bump docker/setup-buildx-action from 1 to 2 (@dependabot)
- \[Actions](deps)\: Bump docker/login-action from 1 to 2 (@dependabot)
- \[Actions](deps)\: Bump docker/build-push-action from 2 to 3 (@dependabot)