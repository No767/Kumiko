import asyncio
import uuid

import uvloop
from genshin_wish_sim_utils import KumikoWSUtils

wsUtils = KumikoWSUtils()


async def addItem():
    await wsUtils.addWSItem(
        item_uuid=str(uuid.uuid4()), name="Roger Bow", star_rank=4, item_type="weapon"
    )


asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
asyncio.run(addItem())
