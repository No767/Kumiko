import orjson
from discord import PartialEmoji, app_commands
from discord.ext import commands
from kumikocore import KumikoCore
from libs.ui.dictionary import DictPages, JapaneseDictPages
from libs.utils import GuildContext
from typing_extensions import Annotated
from yarl import URL


class Dictionary(commands.Cog):
    """Commands to search definitions of words"""

    def __init__(self, bot: KumikoCore) -> None:
        self.bot = bot
        self.session = self.bot.session

    @property
    def display_emoji(self) -> PartialEmoji:
        return PartialEmoji(name="\U0001f4d6")

    @commands.hybrid_group(name="define", fallback="english")
    @app_commands.describe(query="The word to define")
    async def define(
        self, ctx: GuildContext, *, query: Annotated[str, commands.clean_content]
    ) -> None:
        """Define a word from the English dictionary"""
        url = URL("https://api.dictionaryapi.dev/api/v2/entries/en") / query
        async with self.session.get(url) as r:
            data = await r.json(loads=orjson.loads)
            if "message" in data:
                await ctx.send("No results found")
                return
            pages = DictPages(data, ctx=ctx)
            await pages.start()

    @define.command(name="japanese", aliases=["ja", "jp"])
    @app_commands.describe(
        query="The word to define. This can be both in English or Japanese (romaji works)"
    )
    async def japanese(
        self, ctx: GuildContext, *, query: Annotated[str, commands.clean_content]
    ) -> None:
        """Get the definition of a word from the Japanese dictionary"""
        params = {"keyword": query}

        async with self.session.get(
            "https://jisho.org/api/v1/search/words", params=params
        ) as r:
            data = await r.json(loads=orjson.loads)
            if len(data["data"]) == 0:
                await ctx.send("No results found.")
                return
            pages = JapaneseDictPages(data["data"], ctx=ctx)
            await pages.start()


async def setup(bot: KumikoCore) -> None:
    await bot.add_cog(Dictionary(bot))
