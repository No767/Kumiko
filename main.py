import discord
from discord.ext.commands import Bot
from discord import Intents
import os
from dotenv import load_dotenv
load_dotenv()
TOKEN = os.getenv("TOKEN") #just grabs the discord token from a .env file
intents = Intents.all()
bot = Bot(intents=intents, command_prefix='$') # or whatever prefix you choose(!,%,?)

@bot.command(name='info')
async def fetchServerInfo(context):
    info = context.info
    await context.send(f'Server Name: {info.name}')
    await context.send(f'Server Size: {len(info.members)}')
    await context.send(f'Server Name: {info.owner.display_name}')
        
        
        
        
        
class MyClient(discord.Client):
    @bot.event
    async def on_message(message):
	    if message.content == '$hello':
		    await message.channel.send('Hello there')

bot.run(TOKEN) #Make sure not to forget thtis....