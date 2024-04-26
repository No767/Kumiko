from typing import List

import discord
from discord.ext import commands
from libs.utils.pages import KumikoPages, SimplePageSource

from .structs import SimplePrideProfileEntry, SimpleViewsEntry
from .utils import SimplePrideProfilesPageEntry, ViewsPrideProfilesPageEntry


class PrideProfileSearchPages(KumikoPages):
    def __init__(
        self,
        entries: List[SimplePrideProfileEntry],
        *,
        ctx: commands.Context,
        per_page=1
    ):
        converted = [SimplePrideProfilesPageEntry(entry) for entry in entries]
        super().__init__(
            SimplePageSource(converted, per_page=per_page), ctx=ctx, compact=True
        )
        self.embed = discord.Embed(colour=discord.Colour.from_rgb(217, 156, 255))


class PrideProfileStatsPages(KumikoPages):
    def __init__(
        self, entries: List[SimpleViewsEntry], *, ctx: commands.Context, per_page=1
    ):
        converted = [ViewsPrideProfilesPageEntry(entry) for entry in entries]
        super().__init__(
            SimplePageSource(converted, per_page=per_page), ctx=ctx, compact=True
        )
        self.embed = discord.Embed(colour=discord.Colour.from_rgb(217, 156, 255))
