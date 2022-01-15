import asyncio
import random

import discord
import uvloop
from discord.ext import commands


def discord_colors():
    colors = [0x8B77BE, 0xA189E2, 0xCF91D1, 0x5665AA, 0xA3A3D2]
    return random.choice(colors)


class clearMessages(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.is_owner()
    @commands.command(
        name="clear",
        help="Clears number of messages specified from the channel in which the command was called",
    )
    async def clear(self, ctx, number_of_messages: int):
        await ctx.channel.purge(limit=number_of_messages + 1)
        embedVar = discord.Embed(color=discord_colors())
        embedVar.description = f"{number_of_messages} messages were deleted"
        await ctx.send(
            embed=embedVar,
            delete_after=3,
        )

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    @clear.error
    async def on_message_error(
        self, ctx: commands.Context, error: commands.CommandError
    ):
        if isinstance(error, commands.MissingRequiredArgument):
            embedVar = discord.Embed(color=discord.Color.from_rgb(255, 51, 51))
            embedVar.description = f"Missing a required argument: {error.param}"
            embedVar.set_footer(
                text="This only clears messages **before** this command is used"
            )
            msg = await ctx.send(embed=embedVar, delete_after=10)
            await msg.delete(delay=10)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


def setup(bot):
    bot.add_cog(clearMessages(bot))
