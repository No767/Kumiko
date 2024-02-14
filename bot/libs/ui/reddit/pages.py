from typing import List

import discord
from discord.ext.commands import Context
from libs.utils.pages import EmbedListSource, KumikoPages

from .structs import RedditEntry, RedditMemeEntry
from .utils import RedditMemePageEntry, RedditPageEntry


class RedditPages(KumikoPages):
    def __init__(self, entries: List[RedditEntry], *, ctx: Context, per_page: int = 1):
        converted = [RedditPageEntry(entry).to_dict() for entry in entries]
        super().__init__(EmbedListSource(converted, per_page=per_page), ctx=ctx)
        self.embed = discord.Embed(colour=discord.Colour.from_rgb(255, 125, 212))


class RedditMemePages(KumikoPages):
    def __init__(
        self, entries: List[RedditMemeEntry], *, ctx: Context, per_page: int = 1
    ):
        converted = [RedditMemePageEntry(entry).to_dict() for entry in entries]
        super().__init__(EmbedListSource(converted, per_page=per_page), ctx=ctx)
        self.embed = discord.Embed(colour=discord.Colour.from_rgb(255, 125, 212))
