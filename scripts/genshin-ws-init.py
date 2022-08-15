import asyncio
import os
import sys
from pathlib import Path

import uvloop

sys.path.append(os.path.join(os.path.dirname(sys.path[0]), "Bot"))

from dotenv import load_dotenv
from genshin_wish_sim_utils import KumikoWSUtils

mainPath = Path(__file__).parents[1]
envPath = os.path.join(mainPath, "Bot", ".env")

load_dotenv(envPath)
wsUtils = KumikoWSUtils()

POSTGRES_PASSWORD = os.getenv("Postgres_Password_Dev")
POSTGRES_SERVER_IP = os.getenv("Postgres_Server_IP_Dev")
POSTGRES_WS_DATABASE = os.getenv("Postgres_Wish_Sim_Database")
POSTGRES_USERNAME = os.getenv("Postgres_Username_Dev")
POSTGRES_PORT = os.getenv("Postgres_Port_Dev")
CONNECTION_URI = f"postgresql+asyncpg://{POSTGRES_USERNAME}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER_IP}:{POSTGRES_PORT}/{POSTGRES_WS_DATABASE}"


async def main():
    await wsUtils.initAllWSTables(uri=CONNECTION_URI)


asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
asyncio.run(main())
