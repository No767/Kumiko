import asyncio

import aiohttp
import discord
import orjson
import simdjson
import uvloop
from discord.commands import slash_command
from discord.ext import commands

parser = simdjson.Parser()


class advice_slip(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(name="advice", description="Gives some advice from Adviceslip")
    async def adviceSlip(self, ctx):
        async with aiohttp.ClientSession(json_serialize=orjson.dumps) as session:
            async with session.get("https://api.adviceslip.com/advice") as r:
                advice_slip = await r.content.read()
                adviceSlipParsed = parser.parse(advice_slip, recursive=True)
                try:
                    embedVar = discord.Embed(
                        color=discord.Color.from_rgb(251, 204, 255)
                    )
                    embedVar.description = f"{adviceSlipParsed['slip']['advice']}"
                    embedVar.set_footer(
                        text=f"Requested by {ctx.user.name}",
                        icon_url=ctx.user.display_avatar,
                    )
                    await ctx.respond(embed=embedVar)
                except Exception as e:
                    embedVar = discord.Embed()
                    embedVar.description = "The query failed. Please try again."
                    embedVar.add_field(name="Reason", value=e, inline=True)
                    await ctx.respond(embed=embedVar)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


def setup(bot):
    bot.add_cog(advice_slip(bot))
