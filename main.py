import discord
from discord.ext.commands import Bot
from discord import Intents
import os
from dotenv import load_dotenv
load_dotenv()
TOKEN = os.getenv("TOKEN")
intents = Intents.all()
bot = Bot(intents=intents, command_prefix='!') # or whatever prefix you choose(!,%,?)

class MyClient(discord.Client):
    @bot.event
    async def on_message(message):
	    if message.content == 'hello':
		    await message.channel.send('Hello there')
    async def on_message(message):
        if message.content == 'info':
            await message.channel.send('Some info here')

bot.run(TOKEN) #Make sure not to forget thtis....