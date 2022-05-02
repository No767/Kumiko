import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

# Grabs the bot's token from the .env file
load_dotenv()
Discord_Bot_Token = os.getenv("Petal")
bot = commands.Bot(help_command=None)

# Loads in all extensions
initial_extensions = [
    "Cogs.kumikoinfo",
    "Cogs.kumikoping",
    "Cogs.kumikohelp",
    "Cogs.reddit",
    "Cogs.mcsrvstats",
    "Cogs.waifu-generator",
    "Cogs.hypixel",
    "Cogs.waifu-pics",
    "Cogs.advice",
    "Cogs.qrcode",
    "Cogs.spiget",
    "Cogs.jikan",
    "Cogs.top-gg",
    "Cogs.global-error-handling",
    "Cogs.kumikoinvite",
    "Cogs.mangadex",
    "Cogs.version",
    "Cogs.twitter",
    "Cogs.youtube",
    # "Cogs.bonk",
    "Cogs.tenor",
    "Cogs.uptime",
    "Cogs.jisho",
    "Cogs.bot-info",
    "Cogs.openai-gpt3",
    "Cogs.help",
    "Cogs.modrinth",
    "Cogs.discord-bots",
    "Cogs.first-frc-events",
    "Cogs.economy.marketplace", 
    "Cogs.economy.users",
    "Cogs.platform"
]
for extension in initial_extensions:
    bot.load_extension(extension)


# Adds in the bot presence
@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="/kumikohelp"))

# Run the bot
bot.run(Discord_Bot_Token)
