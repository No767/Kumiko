from typing import Optional

import discord
import orjson
from discord import app_commands
from discord.ext import commands
from kumikocore import KumikoCore
from Libs.cog_utils.pronouns import parse_pronouns
from Libs.ui.pronouns import PPPages
from Libs.utils import Embed
from yarl import URL


class Pronouns(commands.Cog):
    """Your to-go module for pronouns!

    This module provides a way to view pronouns for others to see. And this is used seriously as a resource for LGBTQ+ folks.
    """

    def __init__(self, bot: KumikoCore) -> None:
        self.bot = bot
        self.session = self.bot.session

    @property
    def display_emoji(self) -> discord.PartialEmoji:
        return discord.PartialEmoji.from_str("<:BlahajTransHeart:1096897624432443392>")

    @commands.hybrid_group(name="pronouns", fallback="get")
    @app_commands.describe(id="The ID of the user")
    async def pronouns(self, ctx: commands.Context, id: str) -> None:
        """Obtains the pronouns of a Discord user from PronounDB

        This is not directly from Discord but a third party extension
        """
        member = self.bot.get_user(int(id))
        if member is None:
            await ctx.send("Could not find member")
            return
        params = {"platform": "discord", "ids": member.id}
        async with self.session.get(
            "https://pronoundb.org/api/v2/lookup", params=params
        ) as r:
            data = await r.json(loads=orjson.loads)
            if len(data) == 0:
                await ctx.send("No pronouns found for these user(s).")
                return
            embed = Embed()
            embed.set_author(
                name=f"{member.global_name}'s pronouns",
                icon_url=member.display_avatar.url,
            )
            embed.description = "\n".join(
                [
                    f"{k}: {parse_pronouns(v)}"
                    for k, v in data[f"{member.id}"]["sets"].items()
                ]
            )
            await ctx.send(embed=embed)

    @pronouns.command(name="terms")
    @app_commands.describe(
        query="The term to search for. If left blank, this will give all of the terms available"
    )
    async def terms(self, ctx: commands.Context, *, query: Optional[str] = None):
        """Searches for terms on Pronouns.page"""
        # TODO - Set up custom language codes and translated versions
        # We need a drop down menu for all of the other languages
        url = URL("https://en.pronouns.page/api/terms")
        if query:
            url = URL("https://en.pronouns.page/api/terms/search") / query
        async with self.session.get(url) as r:
            data = await r.json(loads=orjson.loads)
            if len(data) == 0:
                await ctx.send("The pronouns were not found")
                return
            pages = PPPages(data, ctx=ctx)
            await pages.start()


async def setup(bot: KumikoCore) -> None:
    await bot.add_cog(Pronouns(bot))
