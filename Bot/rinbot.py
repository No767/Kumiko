import discord
from discord import Intents
from discord.ext import commands
from discord import Client
from discord import Game
from discord import Embed, Activity, ActivityType
import os
from dotenv import load_dotenv

# Grabs the bot's token from the .env file
load_dotenv()
TOKEN = os.getenv("TOKEN")
intents = Intents.all()
bot = commands.Bot(command_prefix=".")

# Loads in all extensions
initial_extensions = [
    "Cogs.rininfo",
    "Cogs.plugin_tools",
    "Cogs.global",
    "Cogs.rinping",
    "Cogs.deviantart",
    "Cogs.valid",
    "Cogs.rinhelp",
    "Cogs.twitter",
    "Cogs.reddit",
    "Cogs.disquest",
    "Cogs.images",
    "Cogs.pinger",
    "Cogs.chat",
    "Cogs.invitation",
    "Cogs.jisho",
    "Cogs.translate",
    "Cogs.chat_purge",
    "Cogs.mcsrvstats",
    "Cogs.waifu_generator",
    "Cogs.hypixel",
    "Cogs.waifu-pics",
    "Cogs.advice",
]
for extension in initial_extensions:
    bot.load_extension(extension)


# Adds in the bot presence
@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name=".rinhelp"))


# Run the bot
bot.run(TOKEN)
