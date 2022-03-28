# ✨ Rin V2 ✨

Rin V2 comes with a ton of improvements, and new features as well. Rin V2 will only support slash (`/`) commands from now on out, since the legacy prefix commands are going to be deprecated. Rin V2 is basically the remastered version of Rin V1. Nearly all the cogs have been rewritten to use faster and efficient algorithms and ways to get the data. Below this is all the changes made so far:

# Major Changes

- Migrate to use slash commands. All legacy prefixes used by Rin and Kumiko won't be supported past v2.0.0
- Fully rewrite nearly all of the cogs to use recursive and loops instead - Much faster than v1.4.4

# Changes

## TD;LR
- Upgrade Rin to Pycord v2.0.0 (Beta as of now)
- Dynamically load data compared to statically loading data 
- Use slash commands instead of old legacy commands

## Additions

- Modrinth API Support
- Discord.bots.gg API Support
- First Events API Support
- GitPod support

## Changes
- Upgrade Rin to Pycord v2.0.0b5 (Beta as of now)
- Dynamically load data compared to statically loading data
- Use recursive looping to load data for literally all of the cogs
- Readjust RinHelp to align with V2 commands
- Literally removed over 4,000 lines of code that were used for statically loading the data
- Add in Modrinth API support
- Added even more commands for Reddit Cog
- Use AIOHTTP's Streams API to obtain data instead of using JSON responses
- Add Discord.bots.gg API Support
- Bump Docker image to Python 3.10.4 instead
- Add in First Events API Support
- Move PostgreSQL DB connections to a different server 
- Removed old error catchers 
- Add GitPod support
- Add button interactions for Info Cog
- Remake patch files

## Removals

- Translate, Chat, Global, Pinger, Clear, Server-Info, NB-Pride, and Vaild Cogs have been removed
- Support for legacy prefix
- Pinterest API Support
- Instagram API Support
- Spotify API Support
- DisQuest
- More unused libs
- Some old commands
