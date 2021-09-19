import typing
import discord
from discord.ext import commands
import discord.ext


class ban(commands.Cogs):
    def __init__(self, bot):
        self.bot = bot

    # Use this with caution...
    @commands.command(name="ban")
    async def ban(self, ctx, members: commands.Greedy[discord.Member],
                  delete_days: typing.Optional[int] = 0, *,
                  reason: str):
        for member in members:
            await member.ban(delete_message_days=delete_days, reason=reason)

        await ctx.send(f'{members} was banned for {delete_days} because of {reason}.')


def setup(bot):
    bot.add_cog(ban(bot))
