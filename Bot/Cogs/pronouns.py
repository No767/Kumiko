from typing import Annotated

import discord
import orjson
from discord import app_commands
from discord.ext import commands
from kumikocore import KumikoCore
from Libs.cog_utils.pronouns import parse_pronouns
from Libs.ui.pronouns import (
    PronounsProfileCircleEntry,
    PronounsProfileEntry,
    PronounsProfilePages,
    PronounsValuesEntry,
    PronounsWordsEntry,
)
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

    @pronouns.command(name="profile")
    @app_commands.describe(
        username="The username of the user. These are not Discord usernames, but pronouns.page usernames"
    )
    async def profile(
        self, ctx: commands.Context, *, username: Annotated[str, commands.clean_content]
    ) -> None:
        """Obtains the profile of an Pronouns.page user"""
        url = URL("https://en.pronouns.page/api/profile/get/") / username
        params = {"version": 2}
        async with self.session.get(url, params=params) as r:
            data = await r.json(loads=orjson.loads)
            if len(data) == 0:
                await ctx.send("The pronouns were not found")
                return
            curr_username = data["username"]
            avatar = data["avatar"]
            converted = {
                k: PronounsProfileEntry(
                    username=curr_username,
                    avatar=avatar,
                    locale=k,
                    names=[
                        PronounsValuesEntry(
                            value=name["value"], opinion=name["opinion"]
                        )
                        for name in v["names"]
                    ],
                    pronouns=[
                        PronounsValuesEntry(
                            value=pronoun["value"], opinion=pronoun["opinion"]
                        )
                        for pronoun in v["pronouns"]
                    ],
                    description=v["description"],
                    age=v["age"],
                    links=v["links"],
                    flags=v["flags"],
                    words=[
                        PronounsWordsEntry(
                            header=words["header"],
                            values=[
                                PronounsValuesEntry(
                                    value=value["value"], opinion=value["opinion"]
                                )
                                for value in words["values"]
                            ],
                        )
                        for words in v["words"]
                    ],
                    timezone=v["timezone"]["tz"],
                    circle=[
                        PronounsProfileCircleEntry(
                            username=member["username"],
                            avatar=member["avatar"],
                            mutual=member["circleMutual"],
                            relationship=member["relationship"],
                        )
                        for member in v["circle"]
                    ]
                    if len(v["circle"]) != 0
                    else None,
                )
                for k, v in data["profiles"].items()
            }
            pages = PronounsProfilePages(entries=converted, ctx=ctx)
            await pages.start()


async def setup(bot: KumikoCore) -> None:
    await bot.add_cog(Pronouns(bot))
