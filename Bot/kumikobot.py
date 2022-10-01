import logging
import os
from pathlib import Path

import discord
from discord.ext import commands
from dotenv import load_dotenv

# Grabs the bot's token from the .env file
load_dotenv()
Discord_Bot_Token = os.getenv("Dev_Bot_Token")
intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix=".", intents=intents, help_command=None)

logging.basicConfig(
    level=logging.INFO,
    format="[%(levelname)s] | %(asctime)s >> %(message)s",
    datefmt="[%m/%d/%Y] [%I:%M:%S %p %Z]",
)

# Literally prevent these modules from attempting to log info stuff
logging.getLogger("asyncio_redis").setLevel(logging.WARNING)
logging.getLogger("gql").setLevel(logging.WARNING)

# New system for loading all cogs
path = Path(__file__).parents[0].absolute()
cogsPath = os.path.join(str(path), "Cogs")

cogsList = os.listdir(cogsPath)

for cogDir in cogsList:
    if cogDir not in ["__pycache__"]:
        subCogsList = os.listdir(os.path.join(cogsPath, cogDir))
        for subCogDir in subCogsList:
            if subCogDir not in [
                "__pycache__",
            ] and not subCogDir.endswith(".py"):
                for lastCog in os.listdir(os.path.join(cogsPath, cogDir, subCogDir)):
                    if lastCog not in ["__pycache__", "config"]:
                        logging.debug(
                            f"Loaded Cog: Cogs.{cogDir}.{subCogDir}.{lastCog[:-3]}"
                        )
                        bot.load_extension(
                            f"Cogs.{cogDir}.{subCogDir}.{lastCog[:-3]}", store=False
                        )
            elif subCogDir.endswith(".py"):
                logging.debug(f"Loaded Cog: Cogs.{cogDir}.{subCogDir[:-3]}")
                bot.load_extension(f"Cogs.{cogDir}.{subCogDir[:-3]}", store=False)

# Adds in the bot presence
@bot.event
async def on_ready():
    logging.info("Kumiko is ready to go! All checkers are loaded and ready!")
    await bot.change_presence(
        activity=discord.Activity(type=discord.ActivityType.watching, name="/help")
    )


# Run the bot
bot.run(Discord_Bot_Token)
