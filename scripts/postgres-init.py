import asyncio
import os
import sys
from pathlib import Path

import uvloop
from dotenv import load_dotenv

path = Path(__file__).parents[1]
envPath = os.path.join(str(path), "Bot", ".env")
sys.path.append(os.path.join(str(path), "Bot"))

from admin_logs_utils import KumikoAdminLogsUtils
from economy_utils import (KumikoAuctionHouseUtils, KumikoEcoUserUtils,
                           KumikoQuestsUtils, KumikoUserInvUtils)
from genshin_wish_sim_utils import KumikoWSUtils

load_dotenv(dotenv_path=envPath)

POSTGRES_PASSWORD = os.getenv("Postgres_Password_Dev")
POSTGRES_SERVER_IP = os.getenv("Postgres_Server_IP_Dev")
POSTGRES_USERNAME = os.getenv("Postgres_Username_Dev")
POSTGRES_PORT = os.getenv("Postgres_Port_Dev")
POSTGRES_QUESTS_DATABASE = os.getenv("Postgres_Quests_Database")
POSTGRES_AH_DATABASE = os.getenv("Postgres_Database_AH_Dev")
POSTGRES_DATABASE = os.getenv("Postgres_Database_Dev")
POSTGRES_WS_DATABASE = os.getenv("Postgres_Wish_Sim_Database")
POSTGRES_AL_DATABASE = os.getenv("Postgres_Admin_Logs_Database")
QUESTS_CONNECTION_URI = f"postgresql+asyncpg://{POSTGRES_USERNAME}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER_IP}:{POSTGRES_PORT}/{POSTGRES_QUESTS_DATABASE}"
CONNECTION_URI = f"postgresql+asyncpg://{POSTGRES_USERNAME}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER_IP}:{POSTGRES_PORT}/{POSTGRES_DATABASE}"
AH_CONNECTION_URI = f"postgresql+asyncpg://{POSTGRES_USERNAME}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER_IP}:{POSTGRES_PORT}/{POSTGRES_AH_DATABASE}"
GWS_CONNECTION_URI = f"postgresql+asyncpg://{POSTGRES_USERNAME}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER_IP}:{POSTGRES_PORT}/{POSTGRES_WS_DATABASE}"
AL_CONNECTION_URI = f"postgresql+asyncpg://{POSTGRES_USERNAME}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER_IP}:{POSTGRES_PORT}/{POSTGRES_AL_DATABASE}"

utils = KumikoEcoUserUtils()
ahUtils = KumikoAuctionHouseUtils()
questsUtils = KumikoQuestsUtils()
userInvUtils = KumikoUserInvUtils()
wsUtils = KumikoWSUtils()
alUtils = KumikoAdminLogsUtils(uri=AL_CONNECTION_URI)


async def main():
    await utils.initUserTables(uri=CONNECTION_URI)
    await ahUtils.initAHTables(uri=AH_CONNECTION_URI)
    await userInvUtils.initUserInvTables(uri=CONNECTION_URI)
    await questsUtils.initQuestsTables(uri=QUESTS_CONNECTION_URI)
    await wsUtils.initAllWSTables(uri=GWS_CONNECTION_URI)
    await alUtils.initAllALTables()


asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

if __name__ == "__main__":
    asyncio.run(main())
