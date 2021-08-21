from discord.ext import commands
from discord import Embed
import jisho

class Jisho(commands.Cog):
    def __init__ (self, bot):
        self.bot = bot

    @commands.command(name="jishosearch")
    async def jishosearch (self, ctx, search: str):
        await ctx.send(jisho.search(search))
        
def setup(bot):
    bot.add_cog(Jisho(bot))
    
# Can't find any api wrappers that work