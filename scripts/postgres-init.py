import asyncio
import os
import sys

import uvloop

sys.path.append(os.path.join(os.path.dirname(sys.path[0]), "Bot"))

from economy_utils import KumikoEcoUserUtils

utils = KumikoEcoUserUtils()


async def main():
    await utils.initTables()
    await utils.initInvTables()


asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
asyncio.run(main())
