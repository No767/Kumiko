
import discord
from discord.ext import commands


class BanV1(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Use this with caution...
    @commands.is_owner()
    @commands.command(name="ban")
    async def banUser(self, ctx):
        await ctx.send(discord.Permissions.ban_members())


def setup(bot):
    bot.add_cog(BanV1(bot))
