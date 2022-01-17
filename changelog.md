# TD;LR
- Replace Asyncio with Uvloop (Faster performance)

# Changes
- Make Reddit Cog Completely Async (This should finally speed up performance)
- Make Waifu-Generator Cog Async
- Use lxml for parsing HTML data instead of the default html parser
- Kinda finished the MangaDex Cog (still need to work on the reader)
- Replace Asyncio with Uvloop (Massive performance gains)
- Rewrite DisQuest to handle methods and queries asynchronously
- Adjust methods for DeviantArt Token Refresher to be async
- Rewrite Pinterest Cog to be Async 
- Move Formatters to dev-dependencies section within Pipfile

# Additions
- Tenor API Support
- Uvloop
- Uptime Cmd
- Full MangaDex API Support (Reader not finished)
# Removals
- As always, more unused libs
- Ujson
