import asyncio
import os
import sys
import time
from pathlib import Path

import uvloop
from dotenv import load_dotenv

path = Path(__file__).parents[0]
libsPath = os.path.join(str(path), "Bot", "Libs")
envPath = os.path.join(str(path), "Bot", ".env")
sys.path.append(libsPath)

from admin_logs_utils import KumikoAdminLogsUtils
from economy_utils import (
    KumikoAuctionHouseUtils,
    KumikoEcoUserUtils,
    KumikoQuestsUtils,
    KumikoUserInvUtils,
)
from genshin_wish_sim_utils import KumikoWSUtils

load_dotenv(dotenv_path=envPath)

POSTGRES_PASSWORD = os.getenv("Postgres_Password")
POSTGRES_SERVER_IP = os.getenv("Postgres_Server_IP")
POSTGRES_USERNAME = os.getenv("Postgres_Username")
POSTGRES_PORT = os.getenv("Postgres_Port")
POSTGRES_DATABASE = os.getenv("Postgres_Kumiko_Database")
CONNECTION_URI = f"postgresql+asyncpg://{POSTGRES_USERNAME}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER_IP}:{POSTGRES_PORT}/{POSTGRES_DATABASE}"

utils = KumikoEcoUserUtils()
ahUtils = KumikoAuctionHouseUtils()
questsUtils = KumikoQuestsUtils()
userInvUtils = KumikoUserInvUtils()
wsUtils = KumikoWSUtils()
alUtils = KumikoAdminLogsUtils(uri=CONNECTION_URI)


async def main():
    await utils.initUserTables(uri=CONNECTION_URI)
    await ahUtils.initAHTables(uri=CONNECTION_URI)
    await userInvUtils.initUserInvTables(uri=CONNECTION_URI)
    await questsUtils.initQuestsTables(uri=CONNECTION_URI)
    await wsUtils.initAllWSTables(uri=CONNECTION_URI)
    await alUtils.initAllALTables()
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
