import discord
import orjson
from discord.ext import commands
from kumikocore import KumikoCore


class Pronouns(commands.Cog):
    """Your to-go module for pronouns!

    This module provides a way to set your pronouns for others to see. And this is used seriously as a resource for LGBTQ+ folks.
    """

    def __init__(self, bot: KumikoCore) -> None:
        self.bot = bot
        self.session = self.bot.session

    @property
    def display_emoji(self) -> discord.PartialEmoji:
        return discord.PartialEmoji.from_str("<:BlahajTransHeart:1096897624432443392>")

    @commands.hybrid_group(name="pronouns", fallback="get")
    async def pronouns(
        self, ctx: commands.Context, user: commands.Greedy[discord.User]
    ) -> None:
        """Obtains the pronouns of a Discord user from PronounDB

        This is not directly from Discord but a third party extension
        """
        parsed_users = [item.id for item in user]
        params = {"platform": "discord", "ids": parsed_users}
        async with self.session.get(
            "https://pronoundb.org/api/v2/lookup", params=params
        ) as r:
            data = await r.json(loads=orjson.loads)
            await ctx.send(data)


async def setup(bot: KumikoCore) -> None:
    await bot.add_cog(Pronouns(bot))
