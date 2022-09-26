import asyncio
import os
import sys
import time
from pathlib import Path

import uvloop
from dotenv import load_dotenv

path = Path(__file__).parents[0]
packagePath = os.path.join(str(path), "Bot")
envPath = os.path.join(str(path), "Bot", ".env")
sys.path.append(packagePath)

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
QUESTS_CONNECTION_URI = f"postgresql+asyncpg://{POSTGRES_USERNAME}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER_IP}:{POSTGRES_PORT}/{POSTGRES_QUESTS_DATABASE}"
CONNECTION_URI = f"postgresql+asyncpg://{POSTGRES_USERNAME}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER_IP}:{POSTGRES_PORT}/{POSTGRES_DATABASE}"
AH_CONNECTION_URI = f"postgresql+asyncpg://{POSTGRES_USERNAME}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER_IP}:{POSTGRES_PORT}/{POSTGRES_AH_DATABASE}"
GWS_CONNECTION_URI = f"postgresql+asyncpg://{POSTGRES_USERNAME}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER_IP}:{POSTGRES_PORT}/{POSTGRES_WS_DATABASE}"

utils = KumikoEcoUserUtils()
ahUtils = KumikoAuctionHouseUtils()
questsUtils = KumikoQuestsUtils()
userInvUtils = KumikoUserInvUtils()
wsUtils = KumikoWSUtils()


async def main():
    await utils.initUserTables(uri=CONNECTION_URI)
    await ahUtils.initAHTables(uri=AH_CONNECTION_URI)
    await userInvUtils.initUserInvTables(uri=CONNECTION_URI)
    await questsUtils.initQuestsTables(uri=QUESTS_CONNECTION_URI)
    await wsUtils.initAllWSTables(uri=GWS_CONNECTION_URI)
    print("[DB Seeder] Successfully created all database tables for Kumiko")


asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        print(f"[DB Seeder] Error: {e.__class__.__name__} - {str(e)}")
        print(f"[DB Seeder] Waiting for 5 seconds before retrying")
        time.sleep(5)
        asyncio.run(main())
