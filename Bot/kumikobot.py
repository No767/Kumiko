import logging
import os

import discord
from discord.ext import commands
from dotenv import load_dotenv

# Grabs the bot's token from the .env file
load_dotenv()
Discord_Bot_Token = os.getenv("Petal")
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

# Loads in all extensions
initial_extensions = [
    "Cogs.kumikoinfo",
    "Cogs.kumikoping",
    "Cogs.kumikohelp",
    "Cogs.reddit",
    "Cogs.mcsrvstats",
    "Cogs.waifu",
    "Cogs.hypixel",
    "Cogs.advice",
    "Cogs.spiget",
    "Cogs.myanimelist",
    "Cogs.top-gg",
    "Cogs.global-error-handling",
    "Cogs.kumikoinvite",
    "Cogs.mangadex",
    "Cogs.version",
    "Cogs.twitter",
    "Cogs.youtube",
    "Cogs.bonk",
    "Cogs.tenor",
    "Cogs.uptime",
    "Cogs.jisho",
    "Cogs.bot-info",
    "Cogs.modrinth",
    "Cogs.discord-bots",
    "Cogs.economy.marketplace",
    "Cogs.economy.users",
    "Cogs.kumiko-platform",
    "Cogs.first-frc-events",
    "Cogs.blue-alliance",
    "Cogs.legacy-help",
    "Cogs.github",
    "Cogs.anilist",
    "Cogs.rabbitmq-consumer",
    "Cogs.economy.auction_house",
    "Cogs.gws",
    "Cogs.avatar",
    "Cogs.uwu",
    "Cogs.ah-checker",
    "Cogs.economy.quests",
    "Cogs.twitch",
    "Cogs.quests-checker",
]
for extension in initial_extensions:
    bot.load_extension(extension, store=False)


# Adds in the bot presence
@bot.event
async def on_ready():
    logging.info("Kumiko is ready to go! All events are ready to go")
    await bot.change_presence(
        activity=discord.Activity(type=discord.ActivityType.watching, name="/help")
    )


# Run the bot
bot.run(Discord_Bot_Token)
