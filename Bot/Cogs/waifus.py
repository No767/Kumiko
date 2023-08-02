import random

import orjson
from discord import PartialEmoji
from discord.ext import commands
from kumikocore import KumikoCore
from Libs.utils import Embed
from Libs.utils.pages import EmbedListSource, KumikoPages


class Waifu(commands.Cog):
    """Gives you random waifu pics"""

    def __init__(self, bot: KumikoCore) -> None:
        self.bot = bot
        self.session = self.bot.session

    @property
    def display_emoji(self) -> PartialEmoji:
        return PartialEmoji.from_str("<:UwU:1013221555003719772>")

    @commands.hybrid_group(name="waifu")
    async def waifu(self, ctx: commands.Context) -> None:
        """Waifu waifu waifus Mai Sakurajima is the best"""
        if ctx.invoked_subcommand is None:
            await ctx.send_help(ctx.command)

    @waifu.command(name="one")
    async def random_waifu(self, ctx: commands.Context) -> None:
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
    async def many_random_waifus(self, ctx: commands.Context) -> None:
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
