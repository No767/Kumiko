import discord
from discord import Intents
from discord.ext import commands
from discord import Client
from discord import Game
import os
from dotenv import load_dotenv

# Grabs the bot's token from the .env file
load_dotenv()
TOKEN = os.getenv("TOKEN")
intents = Intents.all()
bot = commands.Bot(command_prefix=".")

# Loads in all extensions
initial_extensions = ['Cogs.rininfo', 'Cogs.plugin_tools', 'Cogs.global', 'Cogs.rinping', 'Cogs.deviantart', 'Cogs.valid', 'Cogs.rinhelp', 'Cogs.twitter', 'Cogs.reddit', 'Cogs.disquest', 'Cogs.images']
for extension in initial_extensions:
    bot.load_extension(extension)

# Add in Playing status
client = discord.Client(activity=discord.Game(name='my game'))

# Run the bot
bot.run(TOKEN)