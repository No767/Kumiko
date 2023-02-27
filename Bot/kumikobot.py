import asyncio
import logging
import os

import discord
import uvloop
from dotenv import load_dotenv
from kumikocore import KumikoCore

load_dotenv()

REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT = os.getenv("REDIS_PORT")

DISCORD_BOT_TOKEN = os.getenv("DEV_BOT_TOKEN")

intents = discord.Intents.default()
intents.members = True
intents.bans = True
intents.guilds = True

bot = KumikoCore(redis_host=REDIS_HOST, redis_port=REDIS_PORT, intents=intents)

logging.basicConfig(
    level=logging.INFO,
    format="[%(levelname)s] | %(asctime)s >> %(message)s",
    datefmt="[%m/%d/%Y] [%I:%M:%S %p %Z]",
)

logging.getLogger("tortoise").setLevel(logging.WARNING)
logging.getLogger("gql").setLevel(logging.WARNING)

if __name__ == "__main__":
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
    bot.run(DISCORD_BOT_TOKEN)
