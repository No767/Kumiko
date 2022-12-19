import asyncio
import logging
import os
import sys
import urllib.parse
from pathlib import Path

import uvloop
from aerich import Command
from dotenv import load_dotenv

path = Path(__file__).parents[1]
envPath = os.path.join(str(path), "Bot", ".env")
sys.path.append(os.path.join(str(path), "Bot"))
sys.path.append(os.path.join(str(path), "Bot", "Libs"))

load_dotenv(dotenv_path=envPath)

POSTGRES_PASSWORD = urllib.parse.quote_plus(os.getenv("Postgres_Password"))
POSTGRES_SERVER_IP = os.getenv("Postgres_Server_IP")
POSTGRES_DATABASE = os.getenv("Postgres_Kumiko_Database")
POSTGRES_USERNAME = os.getenv("Postgres_Username")
POSTGRES_PORT = os.getenv("Postgres_Port")
CONNECTION_URI = f"asyncpg://{POSTGRES_USERNAME}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER_IP}:{POSTGRES_PORT}/{POSTGRES_DATABASE}"
MODELS = [
    "kumiko_genshin_wish_sim.models",
    "kumiko_servers.models",
    "kumiko_admin_logs.models",
    "kumiko_economy.models",
    "aerich.models",
]

TORTOISE_ORM_SETTINGS = {
    "connections": {
        "default": CONNECTION_URI,
    },
    "apps": {
        "models": {"models": MODELS, "default_connection": "default"},
    },
}

logging.basicConfig(
    level=logging.INFO,
    format="[%(levelname)s] | %(asctime)s >> %(message)s",
    datefmt="[%m/%d/%Y] [%I:%M:%S %p %Z]",
)

cmd = Command(tortoise_config=TORTOISE_ORM_SETTINGS)


async def main():
    try:
        await cmd.init_db(safe=True)
        logging.info("Successfully initialized tables")
    except FileExistsError:
        logging.error(
            "Migration file(s) already exist! Consider upgrading instead of initializing the tables"
        )


if __name__ == "__main__":
    with asyncio.Runner(loop_factory=uvloop.new_event_loop) as runner:
        runner.run(main())
