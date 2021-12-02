import discord
from discord import Intents
from discord.ext import commands
import os
from dotenv import load_dotenv

# Grabs the bot's token from the .env file
load_dotenv()
TOKEN = os.getenv("Hanako_Token")
intents = Intents.all()
bot = commands.Bot(command_prefix=".", help_command=None)

# Loads in all extensions
initial_extensions = [
    "Cogs.rininfo",
    "Cogs.plugin_tools",
    "Cogs.global",
    "Cogs.rinping",
    "Cogs.deviantart",
    "Cogs.valid",
    "Cogs.rinhelp",
    "Cogs.reddit",
    "Cogs.pinger",
    "Cogs.chat",
    "Cogs.jisho",
    "Cogs.translate",
    "Cogs.server-info",
    "Cogs.mcsrvstats",
    "Cogs.waifu_generator",
    "Cogs.hypixel",
    "Cogs.waifu-pics",
    "Cogs.advice",
    "Cogs.qrcode",
    "Cogs.spiget",
    "Cogs.jikan",
    "Cogs.nb-pride",
    "Cogs.top-gg",
    "Cogs.global-error-handling",
    "Cogs.spotify",
    "Cogs.pinterest",
    "Cogs.rininvite",
    "Cogs.mangadex",
    "Cogs.version",
    "Cogs.clear",
]
for extension in initial_extensions:
    bot.load_extension(extension)


# Adds in the bot presence
@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=".rinhelp"))


# Run the bot
bot.run(TOKEN)
