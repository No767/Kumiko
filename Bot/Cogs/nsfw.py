from typing import Optional

import orjson
from discord import PartialEmoji, app_commands
from discord.ext import commands
from kumikocore import KumikoCore
from Libs.utils.pages import EmbedListSource, KumikoPages


class NSFW(commands.Cog):
    """NSFW (18+) content"""

    def __init__(self, bot: KumikoCore) -> None:
        self.bot = bot
        self.session = self.bot.session

    @property
    def display_emoji(self) -> PartialEmoji:
        return PartialEmoji(name="\U0001f51e")

    @commands.is_nsfw()
    @app_commands.describe(tag="The tag to search. Leave blank to obtain random images")
    @commands.hybrid_group(name="r34", fallback="get")
    async def r34(self, ctx: commands.Context, *, tag: Optional[str]) -> None:
        """Obtain R34 images"""
        cleanedTag = tag if tag is not None else "all"
        params = {
            "page": "dapi",
            "s": "post",
            "q": "index",
            "tags": cleanedTag,
            "json": 1,
            "limit": 100,
        }
        async with self.session.get(
            "https://api.rule34.xxx/index.php", params=params
        ) as r:
            data = await r.json(loads=orjson.loads)
            formatData = [{"image": item["sample_url"]} for item in data]
            embedSource = EmbedListSource(formatData, per_page=1)
            pages = KumikoPages(source=embedSource, ctx=ctx)
            await pages.start()


async def setup(bot: KumikoCore) -> None:
    await bot.add_cog(NSFW(bot))
