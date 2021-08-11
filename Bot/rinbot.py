import discord
from discord import Intents
from discord.ext import commands
import os
from dotenv import load_dotenv
import datetime
# Grabs the bot's token from the .env file
load_dotenv()
TOKEN = os.getenv("TOKEN")
intents = Intents.all()
bot = commands.Bot(command_prefix=".")

# Loads in all extensions
initial_extensions = ['Cogs.Rin_Info', 'Cogs.Utility', 'Cog.Bot_Admin', 'Cogs.Misc']
for extension in initial_extensions:
    bot.load_extension(extension)

bot.run(TOKEN)