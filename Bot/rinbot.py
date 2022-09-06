import logging
import os
from pathlib import Path

import discord
from discord.ext import commands
from dotenv import load_dotenv

# Grabs the bot's token from the .env file
load_dotenv()
TOKEN = os.getenv("TOKEN")
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix=".", intents=intents, help_command=None)

logging.basicConfig(
    level=logging.INFO,
    format="[%(levelname)s] | %(asctime)s >> %(message)s",
    datefmt="[%m/%d/%Y] [%I:%M:%S %p %Z]",
)
logging.getLogger("gql").setLevel(logging.WARNING)

# Loads all Cogs from the Cogs folder
path = Path(__file__).parent.resolve()
cogsList = os.listdir(os.path.join(path, "Cogs"))
for items in cogsList:
    if items.endswith(".py"):
        bot.load_extension(f"Cogs.{items[:-3]}")

# Adds in the bot presence
@bot.event
async def on_ready():
    logging.info("Rin is ready to go!")
    await bot.change_presence(
        activity=discord.Activity(type=discord.ActivityType.watching, name="/help")
    )


# Run the bot
bot.run(TOKEN)
