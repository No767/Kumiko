import asyncio

import aiohttp
import discord
import orjson
import uvloop
from discord.ext import commands


class advice_slip(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="advice")
    async def on_message(self, ctx):
        async with aiohttp.ClientSession(json_serialize=orjson.dumps) as session:
            async with session.get("https://api.adviceslip.com/advice") as r:
                advice_slip = await r.text()
                advice_slip_formatted = orjson.loads(advice_slip)
                try:
                    embedVar = discord.Embed(
                        color=discord.Color.from_rgb(251, 204, 255)
                    )
                    embedVar.description = f"{advice_slip_formatted['slip']['advice']}"
                    embedVar.set_footer(
                        text=f"Requested by {ctx.message.author.name}",
                        icon_url=ctx.message.author.avatar_url,
                    )
                    await ctx.send(embed=embedVar)
                except Exception as e:
                    embedVar = discord.Embed()
                    embedVar.description = "The query failed. Please try again."
                    embedVar.add_field(name="Reason", value=e, inline=True)
                    await ctx.send(embed=embedVar)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


def setup(bot):
    bot.add_cog(advice_slip(bot))
