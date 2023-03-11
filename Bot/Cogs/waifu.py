import asyncio
import random

import aiohttp
import discord
import orjson
import simdjson
import uvloop
from discord.commands import SlashCommandGroup
from discord.ext import commands, pages
from numpy.random import default_rng
from rin_exceptions import NotFoundHTTPException

parser = simdjson.Parser()


class Waifu(commands.Cog):
    """Commands for getting pictures of Waifus from multiple places"""

    def __init__(self, bot):
        self.bot = bot

    waifu = SlashCommandGroup("waifu", "Commands to get a ton of waifu stuff")
    waifuRandom = waifu.create_subgroup("random", "Get a random waifu")

    @waifuRandom.command(name="one")
    async def waifuPic(self, ctx):
        """Gets one random waifu pics"""
        waifuTagList = [
            "uniform",
            "maid",
            "waifu",
            "marin-kitagawa",
            "mori-calliope",
            "raiden-shogun",
            "selfies",
        ]

        async with aiohttp.ClientSession(json_serialize=orjson.dumps) as session:
            params = {
                "selected_tags": random.choice(waifuTagList),  # nosec B311
                "is_nsfw": "false",
                "excluded_tags": "oppai",
            }
            async with session.get("https://api.waifu.im/random/", params=params) as r:
                data = await r.content.read()
                dataMain = parser.parse(data, recursive=True)
                try:
                    if r.status in [404, 422]:
                        raise NotFoundHTTPException
                    else:
                        embed = discord.Embed()
                        for mainItem in dataMain["images"]:
                            embed.set_image(url=mainItem["url"])
                            embed.set_footer(text=mainItem["source"])
                        await ctx.respond(embed=embed)
                except NotFoundHTTPException:
                    await ctx.respond(
                        embed=discord.Embed(
                            description="It seems like there were no waifus found... Please try again"
                        )
                    )

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    @waifuRandom.command(name="many")
    async def waifuRandomMany(self, ctx):
        """Returns many random waifu pics"""
        waifuTagList = [
            "uniform",
            "maid",
            "waifu",
            "marin-kitagawa",
            "mori-calliope",
            "raiden-shogun",
            "selfies",
        ]
        default_rng()
        async with aiohttp.ClientSession(json_serialize=orjson.dumps) as session:
            params = {
                "selected_tags": random.choice(waifuTagList),  # nosec B311
                "is_nsfw": "false",
                "excluded_tags": "oppai",
                "many": "true",
            }
            async with session.get("https://api.waifu.im/random/", params=params) as r:
                data = await r.content.read()
                dataMain = parser.parse(data, recursive=True)
                try:
                    if r.status in [404, 422]:
                        raise NotFoundHTTPException
                    else:
                        mainPages = pages.Paginator(
                            pages=[
                                discord.Embed()
                                .set_footer(text=mainItem["source"])
                                .set_image(url=mainItem["url"])
                                for mainItem in dataMain["images"]
                            ]
                        )
                        await mainPages.respond(ctx.interaction, ephemeral=False)
                except NotFoundHTTPException:
                    await ctx.respond(
                        embed=discord.Embed(
                            description="It seems like there were no waifus found... Please try again"
                        )
                    )

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


def setup(bot):
    bot.add_cog(Waifu(bot))
