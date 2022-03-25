# Rin V2

Rin V2 comes with a ton of improvements, and new features as well. Rin V2 will only support slash (`/`) commands from now on out, since the legacy prefix commands are going to be deprecated. Below this is all of the changes made so far

# Major Changes

- Migrate to use slash commands. All legacy prefixes used by Rin and Kumiko won't be supported past v2.0.0
- Fully rewrite nearly all of the cogs to use recursive and loops instead - Much faster than v1.4.4

# Changes

## TD;LR
- Upgrade Rin to Pycord v2.0.0 (Beta as of now)
- Dynamically load data compared to statically loading data 
- Use Slash Commands instead of old legacy commands

## Additions

- Modrinth API Support

## Changes
- Upgrade Rin to Pycord v2.0.0 (Beta as of now)
- Dynamically load data compared to statically loading data
- Use Recursion looping to load data for Twitter, Jikan, Topgg, and other cogs
- Readjust RinHelp to align with V2 commands
- Literally removed over 4,000 lines of code that were used for statically loading the data
- Add in Modrinth API Support
- Added even more commands for Reddit Cog
- Use AIOHTTP's Streams API to obtain data instead of using JSON responses

## Removals

- Translate, Chat, Global, Pinger, Clear, Server-Info, NB-Pride, and Vaild Cogs have been removed
- Support for legacy prefix
- Pinterest API Support
- Instagram API Support
- Spotify API Support
- DisQuest
