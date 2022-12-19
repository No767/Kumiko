import asyncio
import logging
import os
import sys
import time
from pathlib import Path

import uvloop
from dotenv import load_dotenv

path = Path(__file__).parent
libsPath = os.path.join(str(path), "Bot", "Libs")
envPath = os.path.join(str(path), "Bot", ".env")
sys.path.append(libsPath)

from kumiko_economy_utils import (
    KumikoAuctionHouseUtils,
    KumikoEcoUserUtils,
    KumikoQuestsUtils,
    KumikoUserInvUtils,
)

load_dotenv(dotenv_path=envPath)

POSTGRES_PASSWORD = os.getenv("Postgres_Password")
POSTGRES_SERVER_IP = os.getenv("Postgres_Server_IP")
POSTGRES_USERNAME = os.getenv("Postgres_Username")
POSTGRES_PORT = os.getenv("Postgres_Port")
POSTGRES_DATABASE = os.getenv("Postgres_Kumiko_Database")
CONNECTION_URI = f"postgresql+asyncpg://{POSTGRES_USERNAME}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER_IP}:{POSTGRES_PORT}/{POSTGRES_DATABASE}"

logging.basicConfig(
    level=logging.INFO,
    format="[%(levelname)s] | %(asctime)s >> [DB Seeder V1] %(message)s",
    datefmt="[%m/%d/%Y] [%I:%M:%S %p %Z]",
)

utils = KumikoEcoUserUtils()
ahUtils = KumikoAuctionHouseUtils()
questsUtils = KumikoQuestsUtils()
userInvUtils = KumikoUserInvUtils()


async def main():
    await utils.initUserTables(uri=CONNECTION_URI)
    await ahUtils.initAHTables(uri=CONNECTION_URI)
    await userInvUtils.initUserInvTables(uri=CONNECTION_URI)
    await questsUtils.initQuestsTables(uri=CONNECTION_URI)
    logging.info("Successfully created all database tables for Kumiko")


if __name__ == "__main__":
    try:
        with asyncio.Runner(loop_factory=uvloop.new_event_loop) as runner:
            runner.run(main())
    except Exception as e:
        print(f"[DB Seeder] Error: {e.__class__.__name__} - {str(e)}")
        print(f"[DB Seeder] Waiting for 5 seconds before retrying")
        time.sleep(5)
        asyncio.run(main())
