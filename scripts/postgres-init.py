import asyncio

import uvloop

from Bot.economy_utils import KumikoEcoUserUtils

utils = KumikoEcoUserUtils()


async def main():
    await utils.initTables()


asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
asyncio.run(main())
