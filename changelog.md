**Note that this release of Kumiko is coincided with Rin v1.4.0-dev**

# TD;LR
- Replace Asyncio with Uvloop (Faster performance)
- Add the beginnings of the economy system

# Changes
- Make Reddit Cog Completely Async (This should finally speed up performance)
- Make Waifu-Generator Cog Async
- Use lxml for parsing HTML data instead of the default html parser
- Kinda finished the MangaDex Cog (still need to work on the reader)
- Replace Asyncio with Uvloop (Massive performance gains)
- Rewrite DisQuest to handle methods and queries asynchronously
- Adjust methods for DeviantArt Token Refresher to be async
- Rewrite Pinterest Cog to be Async 
- Add Bonk Cmd
- Add Economy System (the base of the economy system)
- Move Formatters to dev-dependencies section within Pipfile
- Require DeviantArt Token Refresher to handle DB connections and queries asynchronously
- Phase out Ujson as the main JSON parser
- Bump Pillow to 9.0.0 to avoid security vulnerabilities

# Additions
- Tenor API Support
- Uvloop
- Uptime Cmd
- Mangadex API Support

# Removals
- As always, more unused libs
- Ujson
