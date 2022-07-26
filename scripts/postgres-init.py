import asyncio
import os
import sys

import uvloop

sys.path.append(os.path.join(os.path.dirname(sys.path[0]), "Bot"))

from economy_utils import KumikoAuctionHouseUtils, KumikoEcoUserUtils

utils = KumikoEcoUserUtils()
ahUtils = KumikoAuctionHouseUtils()


async def main():
    await utils.initUserTables()
    await utils.initInvTables()
    await ahUtils.initAHTables()


asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
asyncio.run(main())
