import discord
from discord.ext import commands


class VersionV1(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="version")
    async def version(self, ctx):
        embedVar = discord.Embed()
<<<<<<< HEAD
        embedVar.description = "Build Version: v0.0.1-dev-b1"
=======
        embedVar.description = "Build Version: v1.3.0-dev-b34"
>>>>>>> a5659c14a6103770ed114e62aee8a13b58a89b5d
        await ctx.send(embed=embedVar)


def setup(bot):
    bot.add_cog(VersionV1(bot))
