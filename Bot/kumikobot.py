import asyncio
import logging
import os
import sys
from pathlib import Path

import discord
import uvloop
from dotenv import load_dotenv
from kumikocore import KumikoCore

# Grabs the bot's token from the .env file
load_dotenv()

DISCORD_BOT_TOKEN = os.getenv("Dev_Bot_Token")
IPC_SECRET_KEY = os.getenv("IPC_Secret_Key")
intents = discord.Intents.default()
intents.members = True

path = Path(__file__).parents[0].absolute()
cogsPath = os.path.join(str(path), "Cogs")
libsPath = os.path.join(str(path), "Libs")
sys.path.append(libsPath)

bot = KumikoCore(ipc_key=IPC_SECRET_KEY, intents=intents)

logging.basicConfig(
    level=logging.INFO,
    format="[%(levelname)s] | %(asctime)s >> %(message)s",
    datefmt="[%m/%d/%Y] [%I:%M:%S %p %Z]",
)

# Literally prevent these modules from attempting to log info stuff
logging.getLogger("asyncio_redis").setLevel(logging.WARNING)
logging.getLogger("gql").setLevel(logging.WARNING)

# Run the bot
if __name__ == "__main__":
    # asyncio.run(bot.ipc.start())
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
    bot.run(DISCORD_BOT_TOKEN)
