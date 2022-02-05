import discord
from discord import Intents
from discord.ext import commands
import os
from dotenv import load_dotenv

# Grabs the bot's token from the .env file
load_dotenv()
TOKEN = os.getenv("Kumiko")
intents = Intents.all()
bot = commands.Bot(command_prefix=".", help_command=None)

# Loads in all extensions
initial_extensions = [
    "Cogs.kumikoinfo",
    "Cogs.kumikoping",
    "Cogs.valid",
    "Cogs.kumikohelp",
    "Cogs.reddit",
    "Cogs.server-info",
    "Cogs.mcsrvstats",
    "Cogs.waifu-generator",
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
    "Cogs.kumikoinvite",
    "Cogs.mangadex",
    "Cogs.version",
    "Cogs.twitter",
    "Cogs.youtube",
    "Cogs.bonk",
    "Cogs.tenor",
    "Cogs.economy-base",
    "Cogs.uptime",
    "Cogs.jisho",
    "Cogs.mangadex",
    "Cogs.bot-info",
    "Cogs.openai-gpt3",
]
for extension in initial_extensions:
    bot.load_extension(extension)


# Adds in the bot presence
@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=".kumikohelp"))


# Run the bot
bot.run(TOKEN)
