**This is only an alpha release. The source code is stable and updated to match the commits that Rin has. The changes below are marked for Rin v1.3.0**

# TD;LR
- MangaDex API Support (Experimental)
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

# Additions
- MangaDex API Support (This time all of it is completely asynchronous and http requests handled by AIOHTTP instead. This should make getting the images a lot faster)
- Use PyCord instead
- Codeowners (For faster code review if needed)
- orjson (for faster json performance)

# Removals
- Disabled missing commands handler (for discords.com verfication)
- EasyBot.py and EasyBot-Plugins submodule 
- Discord.py (Discord.py is not maintained anymore)
- Docker Workflow
- Unused Libs
