from typing import Optional

import discord
import orjson
from discord import app_commands
from discord.ext import commands
from kumikocore import KumikoCore
from libs.cog_utils.pronouns import parse_pronouns
from libs.ui.pronouns import (
    PronounsInclusiveEntry,
    PronounsInclusivePages,
    PronounsNounsEntry,
    PronounsNounsPages,
    PronounsProfileCircleEntry,
    PronounsProfileEntry,
    PronounsProfilePages,
    PronounsTermsEntry,
    PronounsTermsPages,
    PronounsValuesEntry,
    PronounsWordsEntry,
)
from libs.utils import Embed
from typing_extensions import Annotated
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
        return discord.PartialEmoji.from_str(
            "<:ProgressPrideheart:1053776316438167632>"
        )

    @commands.hybrid_group(name="pronouns", fallback="get")
    @app_commands.describe(member="The member to lookup")
    async def pronouns(self, ctx: commands.Context, member: discord.Member) -> None:
        """Obtains the pronouns of a Discord user from PronounDB

        This is not directly from Discord but a third party extension
        """
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
        await ctx.defer()
        url = URL("https://en.pronouns.page/api/profile/get/") / username
        params = {"version": 2}
        async with self.session.get(url, params=params) as r:
            data = await r.json(loads=orjson.loads)
            if len(data["profiles"]) == 0:
                await ctx.send("The profile was not found")
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

    @pronouns.command(name="terms")
    @app_commands.describe(query="The term to look for")
    async def terms(
        self, ctx: commands.Context, *, query: Optional[str] = None
    ) -> None:
        """Looks up terms from Pronouns.page"""
        url = URL("https://en.pronouns.page/api/terms")
        if query:
            url = url / "search" / query
        async with self.session.get(url) as r:
            data = await r.json(loads=orjson.loads)
            if len(data) == 0:
                await ctx.send("No terms were found")
                return
            converted = [
                PronounsTermsEntry(
                    term=term["term"],
                    original=term["original"] if len(term["original"]) > 0 else None,
                    definition=term["definition"],
                    locale=term["locale"],
                    flags=term["flags"],
                    category=term["category"],
                )
                for term in data
            ]
            pages = PronounsTermsPages(entries=converted, ctx=ctx)
            await pages.start()

    @pronouns.command(name="nouns")
    @app_commands.describe(query="The noun to look for")
    async def nouns(
        self, ctx: commands.Context, *, query: Optional[str] = None
    ) -> None:
        """Looks up nouns on Pronouns.page"""
        url = URL("https://en.pronouns.page/api/nouns")
        if query:
            url = url / "search" / query
        async with self.session.get(url) as r:
            # If people start using this for pronouns, then a generator shows up
            # so that's in case this happens
            if r.content_type == "text/html":
                await ctx.send("Uhhhhhhhhhhhh what mate")
                return
            data = await r.json(loads=orjson.loads)
            if len(data) == 0:
                await ctx.send("No nouns were found")
                return
            converted = [
                PronounsNounsEntry(
                    masc=entry["masc"],
                    fem=entry["fem"],
                    neutr=entry["neutr"],
                    masc_plural=entry["mascPl"],
                    fem_plural=entry["femPl"],
                    neutr_plural=entry["neutrPl"],
                )
                for entry in data
            ]
            pages = PronounsNounsPages(entries=converted, ctx=ctx)
            await pages.start()

    @pronouns.command(name="inclusive")
    @app_commands.describe(term="The inclusive term to look for")
    async def inclusive(
        self, ctx: commands.Context, *, term: Optional[str] = None
    ) -> None:
        """Provides inclusive terms for users"""
        url = URL("https://en.pronouns.page/api/inclusive")
        if term:
            url = url / "search" / term
        async with self.session.get(url) as r:
            data = await r.json(loads=orjson.loads)
            if len(data) == 0:
                await ctx.send("No nouns were found")
                return
            converted = [
                PronounsInclusiveEntry(
                    instead_of=entry["insteadOf"],
                    say=entry["say"],
                    because=entry["because"],
                    categories=entry["categories"],
                    clarification=entry["clarification"],
                )
                for entry in data
            ]
            pages = PronounsInclusivePages(entries=converted, ctx=ctx)
            await pages.start()

    @pronouns.command(name="lookup")
    @app_commands.describe(
        pronouns="The pronouns to look up. These are actual pronouns, such as she/her, and they/them. "
    )
    async def lookup(self, ctx: commands.Context, *, pronouns: str) -> None:
        """Lookup info about the given pronouns

        Pronouns include she/her, they/them and many others. You don't have to use the binary forms (eg they/them), but search them up like 'they' or 'she'
        """
        url = URL("https://en.pronouns.page/api/pronouns/")
        banner_url = URL("https://en.pronouns.page/api/banner/")
        full_url = url / pronouns
        full_banner_url = banner_url / f"{pronouns}.png"
        async with self.session.get(full_url) as r:
            data = await r.json(loads=orjson.loads)
            if data is None:
                await ctx.send("The pronouns requested were not found")
                return
            desc = f"{data['description']}\n\n"

            desc += "**Info**\n"
            desc += (
                f"Aliases: {data['aliases']}\nPronounceable: {data['pronounceable']}\n"
            )
            desc += f"Normative: {data['normative']}\n"
            if len(data["morphemes"]) != 0:
                desc += "\n**Morphemes**\n"
                for k, v in data["morphemes"].items():
                    desc += f"{k.replace('_', ' ').title()}: {v}\n"

            if len(data["pronunciations"]) != 0:
                desc += "\n**Pronunciations**\n"
                for k, v in data["pronunciations"].items():
                    desc += f"{k.replace('_', ' ').title()}: {v}\n"
            embed = Embed()
            embed.title = data["name"]
            embed.description = desc
            embed.add_field(name="Examples", value="\n".join(data["examples"]))
            embed.add_field(
                name="Forms",
                value=f"Third Form: {data['thirdForm']}\nSmall Form: {data['smallForm']}",
            )
            embed.add_field(
                name="Plural?",
                value=f"Plural: {data['plural']}\nHonorific: {data['pluralHonorific']}",
            )
            embed.set_image(url=str(full_banner_url))
            await ctx.send(embed=embed)


async def setup(bot: KumikoCore) -> None:
    await bot.add_cog(Pronouns(bot))
