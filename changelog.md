# Changes
- Use AutoFlake within Lint + Format Workflow
- Reformat Workflow Job Names
- Return Kanji, Hiragana, and Katakana as a list within the Jisho cog
- Return Synopsis and background as a description within the Jikan cog
- Assign aliases for Jisho, Jikan, and DeviantArt cmds
- Use AIOHTTP < 3.7.4.post0 to fix coroutine issues
- Reduce the amount of time needed to build Rin's image by reducing the steps and optimizing the image.
- Reformat MCSrvStat from descriptions into fields
# Additions
- DeviantArt API Support (Actually working for once)
- DeviantArt API Token Refresher
- Spotify API Suppport (WIP)
- Pinterest API Support 
# Removals
- Removed unused dependencies
- Officially drop support for requirements.txt