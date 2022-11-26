import asyncio
import os
import sys
from pathlib import Path

import uvloop
from dotenv import load_dotenv
from tortoise import Tortoise

path = Path(__file__).parents[1]
envPath = os.path.join(str(path), "Bot", ".env")
sys.path.append(os.path.join(str(path), "Bot"))
sys.path.append(os.path.join(str(path), "Bot", "Libs"))

from kumiko_utils import KumikoCM

load_dotenv(dotenv_path=envPath)

POSTGRES_PASSWORD = os.getenv("Postgres_Password")
POSTGRES_SERVER_IP = os.getenv("Postgres_Server_IP")
POSTGRES_USERNAME = os.getenv("Postgres_Username")
POSTGRES_PORT = os.getenv("Postgres_Port")
POSTGRES_DATABASE = os.getenv("Postgres_Kumiko_Database")
CONNECTION_URI = f"asyncpg://{POSTGRES_USERNAME}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER_IP}:{POSTGRES_PORT}/{POSTGRES_DATABASE}"


async def main():
    async with KumikoCM(uri=CONNECTION_URI, models=["genshin_wish_sim.models"]):
        await Tortoise.generate_schemas()
        print("[DB Seeder V2] Successfully generated schemas")


asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

if __name__ == "__main__":
    asyncio.run(main())
