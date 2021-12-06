# Changes
- Updated Translate Cog to work now
- Use PyCord instead of Discord.py
- Officially once and for all, the DeviantArt Token Refresher Cog is working. (Done through SQLAlchemy instead)
# Additions
- MangaDex API Support (This time all of it is completely asynchronous and http requests handled by AIOHTTP instead. This should make getting the images a lot faster)
- Use PyCord instead
# Removals
- Disabled missing commands handler (for discords.com verfication)
- EasyBot.py and EasyBot-Plugins submodule 
- Discord.py (Discord.py is not maintained anymore)
- Docker Workflow