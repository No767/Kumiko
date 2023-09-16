import datetime
from typing import Any, Optional, Union

import discord
from discord.ext import commands, menus
from Libs.utils import format_dt
from Libs.utils.pages import KumikoPages


class InfoPageSource(menus.PageSource):
    def is_paginating(self) -> bool:
        # This forces the buttons to appear even in the front page
        return True

    def get_max_pages(self) -> Optional[int]:
        # There's only one actual page in the front page
        # However we need at least 2 to show all the buttons
        return 2

    async def get_page(self, page_number: int) -> Any:
        # The front page is a dummy
        self.index = page_number
        return self

    def format_date(self, dt: Optional[datetime.datetime]):
        if dt is None:
            return "N/A"
        return f'{format_dt(dt, "F")} ({format_dt(dt, "R")})'

    def format_badges(
        self, ctx: commands.Context, user: Union[discord.Member, discord.User]
    ):
        desc = ""
        badges_to_emoji = {
            "partner": "<:partnernew:754032603081998336>",  # Discord Bots
            "verified_bot_developer": "<:verifiedbotdev:853277205264859156>",  # Discord Bots
            "hypesquad_balance": "<:balance:585763004574859273>",  # Discord Bots
            "hypesquad_bravery": "<:bravery:585763004218343426>",  # Discord Bots
            "hypesquad_brilliance": "<:brilliance:585763004495298575>",  # Discord Bots
            "bug_hunter": "<:bughunter:585765206769139723>",  # Discord Bots
            "hypesquad": "<:hypesquad_events:585765895939424258>",  # Discord Bots
            "early_supporter": " <:supporter:585763690868113455> ",  # Discord Bots
            "bug_hunter_level_2": "<:goldbughunter:853274684337946648>",  # Discord Bots
            "staff": "<:staff_badge:1087023029105725481>",  # R. Danny
            "discord_certified_moderator": "<:certified_mod_badge:1087023030431129641>",  # R. Danny
            "active_developer": "<:active_developer:1087023031332900894>",  # R. Danny
        }

        set_flags = {flag for flag, value in user.public_flags if value}
        subset_flags = set_flags & badges_to_emoji.keys()
        badges = [badges_to_emoji[flag] for flag in subset_flags]

        if ctx.guild is not None and ctx.guild.owner_id == user.id:
            badges.append("<:owner:585789630800986114>")  # Discord Bots

        if (
            ctx.guild is not None
            and isinstance(user, discord.Member)
            and user.premium_since is not None
        ):
            badges.append("<:booster:1087022965775925288>")  # R. Danny

        if badges:
            desc = "".join(badges)

        return desc

    async def format_page(self, menu, page):
        user: Union[discord.Member, discord.User] = menu.entries
        ctx = menu.ctx
        embed: discord.Embed = menu.embed

        embed.title = user.global_name
        embed.set_thumbnail(url=user.display_avatar.url)

        if self.index == 0:
            desc = f"""
            {self.format_badges(ctx, user)}
            
            **User ID**: {user.id}
            **Global Username**: {user.global_name}
            **Display Name**: {user.display_name}
            **Created**: {self.format_date(user.created_at)}
            """
            if isinstance(user, discord.Member):
                desc += f"**Joined**: {self.format_date(user.joined_at)}"
            embed.description = desc
        elif self.index == 1:
            desc = f"""
            **Is Bot?**: {user.bot}
            **Is Discord?** {user.system}
            **Mutual Guilds**: {', '.join([guild.name for guild in user.mutual_guilds]).rstrip(',')}
            """
            if isinstance(user, discord.Member):
                desc += f"""
                **Status**: {user.status}
                **Current Voice State**: {user.voice or None}
                """
            embed.description = desc
        return embed


class InfoPages(KumikoPages):
    def __init__(
        self,
        entries: Union[discord.Member, discord.User],
        *,
        ctx: commands.Context,
        per_page: int = 1,
    ):
        self.entries = entries
        self.ctx = ctx
        super().__init__(InfoPageSource(), ctx=ctx, compact=True)
        self.embed = discord.Embed(colour=discord.Colour.from_rgb(255, 125, 212))
