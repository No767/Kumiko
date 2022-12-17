import asyncio
import os
import sys
from pathlib import Path

import uvloop
from dotenv import load_dotenv

path = Path(__file__).parents[1]
envPath = os.path.join(str(path), "Bot", ".env")
sys.path.append(os.path.join(str(path), "Bot"))
sys.path.append(os.path.join(str(path), "Bot", "Libs"))

from kumiko_economy import (
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

utils = KumikoEcoUserUtils()
ahUtils = KumikoAuctionHouseUtils()
questsUtils = KumikoQuestsUtils()
userInvUtils = KumikoUserInvUtils()


async def main():
    await utils.initUserTables(uri=CONNECTION_URI)
    await ahUtils.initAHTables(uri=CONNECTION_URI)
    await userInvUtils.initUserInvTables(uri=CONNECTION_URI)
    await questsUtils.initQuestsTables(uri=CONNECTION_URI)


asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

if __name__ == "__main__":
    asyncio.run(main())
