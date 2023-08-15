import random
from typing import Optional

import orjson
from discord import PartialEmoji, app_commands
from discord.ext import commands
from kumikocore import KumikoCore
from Libs.ui.nsfw import R34DownloadView
from Libs.utils import Embed
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
        cleaned_tag = (
            f"{tag} -ai_generated* -stable_diffusion" if tag is not None else "all"
        )
        params = {
            "page": "dapi",
            "s": "post",
            "q": "index",
            "tags": cleaned_tag,
            "json": 1,
            "limit": 100,
        }
        async with self.session.get(
            "https://api.rule34.xxx/index.php", params=params
        ) as r:
            data = await r.json(loads=orjson.loads)
            format_data = [{"image": item["sample_url"]} for item in data]
            embed_source = EmbedListSource(format_data, per_page=1)
            pages = KumikoPages(source=embed_source, ctx=ctx)
            await pages.start()

    @commands.is_nsfw()
    @r34.command(name="random")
    async def random(self, ctx: commands.Context) -> None:
        """Get a random R34 image"""
        await ctx.defer()
        params = {
            "page": "dapi",
            "s": "post",
            "q": "index",
            "json": 1,
            "pid": random.randint(1, 25),
            "limit": 50,
            "tags": "-ai_generated* -stable_diffusion",  # Block AI generated images
        }
        async with self.session.get(
            "https://api.rule34.xxx/index.php", params=params
        ) as r:
            data = await r.json(loads=orjson.loads)
            random_pick = random.choice(data)
            embed = Embed()
            view = R34DownloadView(link=random_pick["file_url"])
            embed.set_footer(text=f"Source: {random_pick['source'] or None}")
            embed.set_image(url=random_pick["sample_url"])
            await ctx.send(embed=embed, view=view)


async def setup(bot: KumikoCore) -> None:
    await bot.add_cog(NSFW(bot))
