import asyncio

import discord
import uvloop
from discord.commands import slash_command
from discord.ext import commands


class rinping(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(name="ping", description="Measures the ping of Rin")
    async def on_message(self, ctx):
        try:
            ping_embed = discord.Embed()
            ping_embed.description = f"Ping >> {round(self.bot.latency * 1000)} ms"
            await ctx.send(embed=ping_embed)
        except Exception as e:
            ping_embed = discord.Embed()
            ping_embed.description = "The command was not successful"
            ping_embed.add_field(name="Reason", value=e, inline=True)
            await ctx.respond(embed=ping_embed)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


def setup(bot):
    bot.add_cog(rinping(bot))
