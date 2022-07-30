import asyncio
import os
import sys

import uvloop

sys.path.append(os.path.join(os.path.dirname(sys.path[0]), "Bot"))

from economy_utils import (KumikoAuctionHouseUtils, KumikoEcoUserUtils,
                           KumikoQuestsUtils)

POSTGRES_PASSWORD = os.getenv("Postgres_Password_Dev")
POSTGRES_SERVER_IP = os.getenv("Postgres_Server_IP_Dev")
POSTGRES_QUESTS_DATABASE = os.getenv("Postgres_Quests_Database")
POSTGRES_USERNAME = os.getenv("Postgres_Username_Dev")
CONNECTION_URI = f"postgresql+asyncpg://{POSTGRES_USERNAME}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER_IP}:5432/{POSTGRES_QUESTS_DATABASE}"

utils = KumikoEcoUserUtils()
ahUtils = KumikoAuctionHouseUtils()
questsUtils = KumikoQuestsUtils()


async def main():
    # await utils.initUserTables()
    # await utils.initInvTables()
    # await ahUtils.initAHTables()
    await questsUtils.initQuestsTables(CONNECTION_URI)


asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
asyncio.run(main())
