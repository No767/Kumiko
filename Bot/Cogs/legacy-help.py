import discord
from discord.ext import commands


class LegacyHelpCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="help")
    async def legacyHelper(self, ctx):
        embed = discord.Embed()
        embed.description = "Hey there, Rin has moved from the old prefix (`.`) to slash commands (`/`). In order to get started, use `/help` or `/rinhelp` instead of `.help`."
        await ctx.send(embed=embed)

    @commands.command(name="rinhelp")
    async def legacyHelper2(self, ctx):
        embed = discord.Embed()
        embed.description = "Hey there, Rin has moved from the old prefix (`.`) to slash commands (`/`). In order to get started, use `/help` or `/rinhelp` instead of `.help`."
        await ctx.send(embed=embed)

    @commands.command(name="info")
    async def legacyHelper3(self, ctx):
        embed = discord.Embed()
        embed.description = "Hey there, Rin has moved from the old prefix (`.`) to slash commands (`/`). In order to get started, use `/help` or `/rinhelp` instead of `.help`."
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(LegacyHelpCommand(bot))
