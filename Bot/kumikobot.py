import asyncio
import logging
import os
import sys
import urllib.parse
from pathlib import Path

import discord
import uvloop
from dotenv import load_dotenv
from kumikocore import KumikoCore

# Grabs the bot's token from the .env file
load_dotenv()

REDIS_HOST = os.getenv("Redis_Server_IP")
REDIS_PORT = os.getenv("Redis_Port")
POSTGRES_PASSWORD = urllib.parse.quote_plus(os.getenv("Postgres_Password"))
POSTGRES_SERVER_IP = os.getenv("Postgres_Server_IP")
POSTGRES_DB = os.getenv("Postgres_Kumiko_Database")
POSTGRES_PORT = os.getenv("Postgres_Port")
POSTGRES_USERNAME = os.getenv("Postgres_Username")
CONNECTION_URI = f"asyncpg://{POSTGRES_USERNAME}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER_IP}:{POSTGRES_PORT}/{POSTGRES_DB}"
MODELS = [
    "kumiko_genshin_wish_sim.models",
    "kumiko_servers.models",
    "kumiko_economy.models",
]

DISCORD_BOT_TOKEN = os.getenv("Dev_Bot_Token")
IPC_SECRET_KEY = os.getenv("IPC_Secret_Key")

intents = discord.Intents.default()
intents.members = True
intents.bans = True
intents.guilds = True

path = Path(__file__).parents[0].absolute()
cogsPath = os.path.join(str(path), "Cogs")
libsPath = os.path.join(str(path), "Libs")
sys.path.append(libsPath)

bot = KumikoCore(
    uri=CONNECTION_URI,
    models=MODELS,
    redis_host=REDIS_HOST,
    redis_port=REDIS_PORT,
    ipc_secret_key=IPC_SECRET_KEY,
    intents=intents,
)

logging.basicConfig(
    level=logging.INFO,
    format="[%(levelname)s] | %(asctime)s >> %(message)s",
    datefmt="[%m/%d/%Y] [%I:%M:%S %p %Z]",
)

# Literally prevent these modules from attempting to log info stuff
logging.getLogger("tortoise").setLevel(logging.WARNING)
logging.getLogger("gql").setLevel(logging.WARNING)

# Run the bot
if __name__ == "__main__":
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
    bot.run(DISCORD_BOT_TOKEN)
