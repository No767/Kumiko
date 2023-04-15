import random

import orjson
from discord.ext import commands
from kumikocore import KumikoCore
from Libs.utils import Embed
from Libs.utils.pages import EmbedListSource, KumikoPages


class Waifu(commands.Cog):
    """Commands for getting some waifu pics"""

    def __init__(self, bot: KumikoCore) -> None:
        self.bot = bot
        self.session = self.bot.session

    @commands.hybrid_group(name="waifu")
    async def waifu(self, ctx: commands.Context) -> None:
        """Base parent command for waifu - See the subcommands for more info"""
        if ctx.invoked_subcommand is None:
            await ctx.send_help(ctx.command)

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
        params = {
            "included_tags": random.choice(waifuTagList),
            "is_nsfw": "false",
            "excluded_tags": "oppai",
        }
        async with self.session.get("https://api.waifu.im/search/", params=params) as r:
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
        params = {
            "included_tags": random.choice(waifuTagList),
            "is_nsfw": "False",
            "excluded_tags": "oppai",
            "many": "true",
        }
        async with self.session.get("https://api.waifu.im/search/", params=params) as r:
            data = await r.json(loads=orjson.loads)
            mainData = [{"image": item["url"]} for item in data["images"]]
            embedSource = EmbedListSource(mainData, per_page=1)
            menu = KumikoPages(source=embedSource, ctx=ctx, compact=False)
            await menu.start()


async def setup(bot: KumikoCore) -> None:
    await bot.add_cog(Waifu(bot))
