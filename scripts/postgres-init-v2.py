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
MODELS = [
    "kumiko_genshin_wish_sim.models",
    "kumiko_servers.models",
    "kumiko_admin_logs.models",
]


async def main():
    async with KumikoCM(uri=CONNECTION_URI, models=MODELS):
        await Tortoise.generate_schemas()
        print("[Postgres Init V2] Successfully generated schemas")


if __name__ == "__main__":
    with asyncio.Runner(loop_factory=uvloop.new_event_loop) as runner:
        runner.run(main())
