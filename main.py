import discord
from discord import Intents
from discord.ext import commands
from discord.abc import User
import os
from dotenv import load_dotenv
import datetime

# Grabs the bot's token from the .env file
load_dotenv()
TOKEN = os.getenv("TOKEN")  
intents = Intents.all()
bot = commands.Bot(command_prefix=".")


@bot.command(name='info')
async def on_message(message):
    embedVar = discord.Embed(title="Info", color=14414079, timestamp= datetime.datetime.now())
    embedVar.add_field(name="Command Prefix", value='Command Prefix is "**.**"')
    embedVar.add_field(name="Server Name", value=message.guild.name)
    await message.channel.send(embed=embedVar)

bot.run(TOKEN)
