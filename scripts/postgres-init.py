import asyncio
import sys

import uvloop

# very hacky solution, probably will not work...
sys.path.insert(0, "/mnt/d/GitHub Repos [Local]/Kumiko/Bot/")

from Bot.economy_utils import KumikoEcoUserUtils

utils = KumikoEcoUserUtils()


async def main():
    await utils.getUser(454357482102587393)


asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
asyncio.run(main())
