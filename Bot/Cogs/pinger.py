import asyncio

import discord
import uvloop
from discord.ext import commands


class rinpinger(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="pinger")
    async def pinger(self, ctx):
        try:
            await ctx.send("Enter the number of times you want to ping someone: ")
            ping = await self.bot.wait_for("message")
            await ctx.send("Enter the user you want to ping: ")
            user = await self.bot.wait_for("message")
            if user.content in ["@everyone", "@here"]:
                await ctx.send("You can't ping everyone")
            else:
                await ctx.send("Enter the reason for the ping: ")
                reason = await self.bot.wait_for("message")
                for _ in range(int(ping.content)):
                    await ctx.send(f"{user} {reason}")
        except Exception as e:
            await ctx.send(f"The pinger cog didnt work. Please try again.\nReason: {e}")

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    @pinger.error
    async def on_message_error(
        self, ctx: commands.Context, error: commands.CommandError
    ):
        if isinstance(error, commands.MissingRequiredArgument):
            embedVar = discord.Embed(color=discord.Color.from_rgb(255, 51, 51))
            embedVar.description = f"Missing a required argument: {error.param}"
            msg = await ctx.send(embed=embedVar, delete_after=10)
            await msg.delete(delay=10)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


def setup(bot):
    bot.add_cog(rinpinger(bot))
