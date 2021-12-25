**This is only an alpha version of Kumiko. All of these changes are from upstream Rin**

# Rin v1.3.0
# TD;LR
- MangaDex API Support (Experimental + Unstable)
- Fix DeviantArt Token Refresher Cog
- Major Performance Improvements (via asynchronous code + faster json lib)

# Changes
- Updated Translate Cog to work now
- Use PyCord instead of Discord.py
- Officially once and for all, the DeviantArt Token Refresher Cog is working. (Done through SQLAlchemy instead)
- Bump to Python 3.10.1
- Fix Snyk workflow secrets issue
- Make McSrvStat and MangaDex async to improve performance
- Rewrite DisQuest to use SQLAlchemy instead of SQLite to prevent SQL Injection attacks
- Move from ujson to orjson for even faster json decoding performance
- Remove Unused Libs
- Changed DeviantArt and DeviantArt Token Refresher Cogs to use PostgreSQL instead of SQLite
- Make Jikan/MAL Cog async to improve performance + use orjson for json serialization
- Rewrite Hypixel and Topgg Cogs to be async for better performance
- Rewrite Spiget Cog to be async for better performance

# Additions
- MangaDex API Support (This time all of it is completely asynchronous and http requests handled by AIOHTTP instead. This should make getting the images a lot faster. Note that the MD Cog is disabled and will be re-enabled once the code is stable)
- Use PyCord instead
- Codeowners (For faster code review if needed)
- orjson (for faster json performance)

# Removals
- Disabled missing commands handler (for discords.com verfication)
- EasyBot.py and EasyBot-Plugins submodule 
- Discord.py (Discord.py is not maintained anymore)
- Docker Workflow
- Unused Libs
- Pinger Cog
- Spiget-Author cmd (causing way too much issues)
- Global Cog (Disabled as of now, will be added to Kumiko later)

# Rin v1.3.1
# Changes
- Remove DisQuest's level up messages
- Remove unused code in the topgg cog
- Re-enabled DisQuest
- Moved all DisQuest Data to PostgreSQL + Fixed rank and globalrank cmds

# Additions
- Alias for `.globalrank` (it's `.grank`)
# Removals
- Remove DisQuest's level up messages (Verifiers for sites like top.gg and others hate annoying pop-up messages, so this has been taken away to prevent that)
- Unused Files