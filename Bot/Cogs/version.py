import discord
from discord.ext import commands


class VersionV1(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="version")
    async def version(self, ctx):
        embedVar = discord.Embed()
        embedVar.description = "Build Version: v1.3.2"
        await ctx.send(embed=embedVar)


def setup(bot):
    bot.add_cog(VersionV1(bot))
