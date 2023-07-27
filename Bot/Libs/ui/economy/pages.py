from typing import List

import discord
from discord.ext import commands
from Libs.utils.pages import KumikoPages, SimplePageSource

from .utils import LeaderboardEntry, LeaderboardPageEntry


class BasePages(KumikoPages):
    def __init__(self, entries, *, ctx: commands.Context, per_page: int = 10):
        super().__init__(SimplePageSource(entries, per_page=per_page), ctx=ctx)
        self.embed = discord.Embed(
            title="Leaderboard stats", colour=discord.Colour.from_rgb(219, 171, 255)
        )


class LeaderboardPages(BasePages):
    def __init__(
        self,
        entries: List[LeaderboardEntry],
        *,
        ctx: commands.Context,
        per_page: int = 10
    ):
        converted = [LeaderboardPageEntry(entry) for entry in entries]
        super().__init__(converted, per_page=per_page, ctx=ctx)
