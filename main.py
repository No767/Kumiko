import discord
from discord import Intents
from discord.ext import commands
import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("TOKEN")  # just grabs the discord token from a .env file
intents = Intents.all()
bot = commands.Bot(command_prefix=".")


@bot.command(name='info')
async def fetchServerInfo(context):
    info = context.info
    await context.send(f'Server Name: {info.name}')
    await context.send(f'Server Size: {len(info.members)}')
    await context.send(f'Server Name: {info.owner.display_name}')

@bot.command()
async def rininfo(ctx):
    await ctx.send(f'Hello There \nThis is the Rin Bot, a bot which uses the EasyBot.py framework')

bot.run(TOKEN)
