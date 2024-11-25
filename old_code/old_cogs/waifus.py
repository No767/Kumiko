import random
from typing import Optional

import orjson
from discord import PartialEmoji, app_commands
from discord.ext import commands
from libs.ui.waifus import NekoImagesPages, NekosImages
from libs.utils import Embed
from libs.utils.pages import EmbedListSource, KumikoPages
from yarl import URL

from bot.kumiko import KumikoCore


class Waifu(commands.Cog):
    """Gives you random waifu pics"""

    def __init__(self, bot: KumikoCore) -> None:
        self.bot = bot
        self.session = self.bot.session

    @property
    def display_emoji(self) -> PartialEmoji:
        return PartialEmoji.from_str("<:UwU:1013221555003719772>")

    @commands.hybrid_group(name="waifu", fallback="one")
    async def waifu(self, ctx: commands.Context) -> None:
        """Gives you a waifu"""
        waifu_list = [
            "uniform",
            "maid",
            "waifu",
            "marin-kitagawa",
            "mori-calliope",
            "raiden-shogun",
            "selfies",
        ]
        params = {
            "included_tags": random.choice(waifu_list),
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
        waifu_list = [
            "uniform",
            "maid",
            "waifu",
            "marin-kitagawa",
            "mori-calliope",
            "raiden-shogun",
            "selfies",
        ]
        params = {
            "included_tags": random.choice(waifu_list),
            "is_nsfw": "False",
            "excluded_tags": "oppai",
            "many": "true",
        }
        async with self.session.get("https://api.waifu.im/search/", params=params) as r:
            data = await r.json(loads=orjson.loads)
            converted_data = [{"image": item["url"]} for item in data["images"]]
            embed_source = EmbedListSource(converted_data, per_page=1)
            menu = KumikoPages(source=embed_source, ctx=ctx, compact=False)
            await menu.start()

    @commands.hybrid_group(name="nekos", fallback="random")
    @app_commands.describe(count="How much neko images do you want?")
    async def neko(
        self,
        ctx: commands.Context,
        count: Optional[app_commands.Range[int, 1, 100]] = 1,
    ) -> None:
        """Random images of anime waifu cats"""
        if count is not None and (count > 100 or count < 1):
            await ctx.send("The min is 1, and the max is 100!")
            return
        url = URL("https://nekos.moe/api/v1/random/image")
        params = {"count": count, "nsfw": 0}
        headers = {"User-Agent": "Kumiko (https://github.com/No767/Kumiko, v0)"}
        async with self.session.get(url, params=params, headers=headers) as r:
            data = await r.json(loads=orjson.loads)
            converted = [
                NekosImages(
                    id=item["id"], tags=item["tags"], created_at=item["createdAt"]
                )
                for item in data["images"]
            ]
            pages = NekoImagesPages(converted, ctx=ctx)
            await pages.start()

    @neko.command(name="lookup")
    @app_commands.describe(tags="A comma separated list of tags (Eg catgirl, maid)")
    async def lookup(self, ctx: commands.Context, *, tags: str) -> None:
        """Looks up for some nekos"""
        tag_list = tags.split(",")
        url = URL("https://nekos.moe/api/v1/images/search")
        params = {"nsfw": 0, "sort": "newest", "limit": 50, "tags": tag_list}
        headers = {"User-Agent": "Kumiko (https://github.com/No767/Kumiko, v0)"}
        async with self.session.post(url, data=params, headers=headers) as r:
            data = await r.json(loads=orjson.loads)
            if len(data) == 0 or "images" not in data:
                await ctx.send("No results found!")
                return
            converted = [
                NekosImages(
                    id=item["id"], tags=item["tags"], created_at=item["createdAt"]
                )
                for item in data["images"]
            ]
            pages = NekoImagesPages(converted, ctx=ctx)
            await pages.start()


async def setup(bot: KumikoCore) -> None:
    await bot.add_cog(Waifu(bot))
