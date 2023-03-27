import random

import aiohttp
import orjson
from discord.ext import commands
from Libs.utils import Embed
from Libs.utils.pages import EmbedListSource, KumikoPages


class Waifu(commands.Cog):
    """Commands for getting some waifu pics"""

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.hybrid_group(name="waifu")
    async def waifu(self, ctx: commands.Context) -> None:
        """Base parent command for waifu - See the subcommands for more info"""
        ...

    @waifu.command(name="one")
    async def randomWaifu(self, ctx: commands.Context) -> None:
        """Returns a random waifu pic"""
        waifuTagList = [
            "uniform",
            "maid",
            "waifu",
            "marin-kitagawa",
            "mori-calliope",
            "raiden-shogun",
            "selfies",
        ]
        async with aiohttp.ClientSession() as session:
            params = {
                "included_tags": random.choice(waifuTagList),
                "is_nsfw": "false",
                "excluded_tags": "oppai",
            }
            async with session.get("https://api.waifu.im/search/", params=params) as r:
                data = await r.json(loads=orjson.loads)
                embed = Embed().set_image(url=data["images"][0]["url"])
                await ctx.send(embed=embed)

    @waifu.command(name="many")
    async def randomWaifuMany(self, ctx: commands.Context) -> None:
        """Returns up to 30 random waifu pics"""
        waifuTagList = [
            "uniform",
            "maid",
            "waifu",
            "marin-kitagawa",
            "mori-calliope",
            "raiden-shogun",
            "selfies",
        ]
        async with aiohttp.ClientSession() as session:
            params = {
                "included_tags": random.choice(waifuTagList),
                "is_nsfw": "False",
                "excluded_tags": "oppai",
                "many": "true",
            }
            async with session.get("https://api.waifu.im/search/", params=params) as r:
                data = await r.json(loads=orjson.loads)
                mainData = [{"image": item["url"]} for item in data["images"]]
                embedSource = EmbedListSource(mainData, per_page=1)
                menu = KumikoPages(source=embedSource, ctx=ctx, compact=False)
                await menu.start()


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Waifu(bot))
