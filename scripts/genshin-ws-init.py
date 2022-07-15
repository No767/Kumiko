import asyncio
import os
import sys

import uvloop

sys.path.append(os.path.join(os.path.dirname(sys.path[0]), "Bot"))

from genshin_wish_sim_utils import KumikoWSUtils

wsUtils = KumikoWSUtils()


async def main():
    await wsUtils.initAllWSTables()


asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
asyncio.run(main())
