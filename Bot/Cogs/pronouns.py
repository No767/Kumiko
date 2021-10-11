from discord.ext import commands
import discord

class check_pronouns(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    # async def on_guild_join(self, ctx):