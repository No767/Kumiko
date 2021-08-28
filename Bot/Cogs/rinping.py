import discord
from discord.ext import commands
from discord import Embed


class rinping(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name="ping",
    )
    async def ping(self, ctx):
        ping_embed = discord.Embed()
        ping_embed.description = f"Ping >> {self.bot.latency} seconds"
        await ctx.send(embed=ping_embed)


def setup(bot):
    bot.add_cog(rinping(bot))
