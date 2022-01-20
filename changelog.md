# TD;LR
- Fix DeviantArt cog breaking due to asyncio issues

# Changes
- Fix where the DeviantArt cog would break due to an asyncio issue (the coroutine needed to be passed as a variable and then indexed)
