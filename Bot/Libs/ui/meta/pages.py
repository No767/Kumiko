import datetime
from typing import Any, Optional, Union

import discord
from discord.ext import commands, menus
from Libs.cog_utils.meta import format_badges
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

    async def format_page(self, menu, page):
        user: Union[discord.Member, discord.User] = menu.entries
        ctx = menu.ctx
        embed: discord.Embed = menu.embed

        embed.title = user.global_name
        embed.set_thumbnail(url=user.display_avatar.url)

        if self.index == 0:
            desc = f"""
            {format_badges(ctx, user)}
            
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
