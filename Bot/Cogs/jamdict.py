from jamdict import Jamdict
from discord.ext import commands
import discord

jam = Jamdict()


class Jamdict(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="jamdict")
    async def on_message(self, ctx, search: str):
        jamdict_search = search
        result = jam.lookup(search)
        embedVar = discord.Embed()
        embedVar.description = f"{result}"
        await ctx.send(embed=embedVar)


def setup(bot):
    bot.add_cog(Jamdict(bot))
