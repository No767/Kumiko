import discord
from discord.ext import commands
from discord import client
from dotenv import load_dotenv
import deviantart
import os
load_dotenv()
Client_ID = os.getenv("Client_ID")
Client_Secret = os.getenv("Client_Secret")
da = deviantart.Api("Client_ID", "Client_Secret")

class deviantart(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    @commands.command(
        name = 'diviantart',
        help = 'Grab art from Devianart'
    )
    
    @client.event
    async def on_message(message):
        if message.content.startswith('.devianart'):
            channel = message.channel
            await channel.send('Please enter in the chat the User that you want to get the art from')
            
