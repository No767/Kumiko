import asyncio
import os
import sys

import uvloop

sys.path.append(os.path.join(os.path.dirname(sys.path[0]), "Bot"))

from economy_utils import (KumikoAuctionHouseUtils, KumikoEcoUserUtils,
                           KumikoQuestsUtils, KumikoUserInvUtils)

POSTGRES_PASSWORD = os.getenv("Postgres_Password_Dev")
POSTGRES_SERVER_IP = os.getenv("Postgres_Server_IP_Dev")
POSTGRES_QUESTS_DATABASE = os.getenv("Postgres_Quests_Database")
POSTGRES_AH_DATABASE = os.getenv("Postgres_Database_AH_Dev")
POSTGRES_DATABASE = os.getenv("Postgres_Database_Dev")
POSTGRES_USERNAME = os.getenv("Postgres_Username_Dev")
QUESTS_CONNECTION_URI = f"postgresql+asyncpg://{POSTGRES_USERNAME}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER_IP}:5432/{POSTGRES_QUESTS_DATABASE}"
CONNECTION_URI = f"postgresql+asyncpg://{POSTGRES_USERNAME}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER_IP}:5432/{POSTGRES_DATABASE}"
AH_CONNECTION_URI = f"postgresql+asyncpg://{POSTGRES_USERNAME}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER_IP}:5432/{POSTGRES_AH_DATABASE}"

utils = KumikoEcoUserUtils()
ahUtils = KumikoAuctionHouseUtils()
questsUtils = KumikoQuestsUtils()
userInvUtils = KumikoUserInvUtils()


async def main():
    await utils.initUserTables(uri=CONNECTION_URI)
    await ahUtils.initAHTables(uri=AH_CONNECTION_URI)
    await userInvUtils.initUserInvTables(uri=CONNECTION_URI)
    await questsUtils.initQuestsTables(uri=QUESTS_CONNECTION_URI)


asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
asyncio.run(main())
