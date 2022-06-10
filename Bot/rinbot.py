import os

import discord
from discord.ext import commands
from dotenv import load_dotenv

# Grabs the bot's token from the .env file
load_dotenv()
TOKEN = os.getenv("Hanako_Token")
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix=".", intents=intents, help_command=None)

# Loads in all extensions
initial_extensions = [
    "Cogs.rininfo",
    "Cogs.rinping",
    "Cogs.rinhelp",
    "Cogs.reddit",
    "Cogs.mcsrvstats",
    "Cogs.waifu-generator",
    "Cogs.hypixel",
    "Cogs.waifu-pics",
    "Cogs.advice",
    "Cogs.qrcode-maker",
    "Cogs.spiget",
    "Cogs.jikan",
    "Cogs.top-gg",
    "Cogs.global-error-handling",
    "Cogs.rininvite",
    "Cogs.version",
    "Cogs.twitter",
    "Cogs.youtube",
    "Cogs.jisho",
    "Cogs.tenor",
    "Cogs.uptime",
    "Cogs.mangadex",
    "Cogs.bot-info",
    "Cogs.help",
    "Cogs.modrinth",
    "Cogs.discord-bots",
    "Cogs.first-frc-events",
    "Cogs.blue-alliance",
    "Cogs.legacy-help",
    "Cogs.github",
    "Cogs.anilist",
]
for extension in initial_extensions:
    bot.load_extension(extension)


# Adds in the bot presence
@bot.event
async def on_ready():
    await bot.change_presence(
        activity=discord.Activity(type=discord.ActivityType.watching, name="/rinhelp")
    )


# Run the bot
bot.run(TOKEN)
