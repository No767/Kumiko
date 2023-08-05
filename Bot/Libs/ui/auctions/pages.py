from typing import List

import asyncpg
from discord.ext import commands
from Libs.utils.pages import EmbedListSource, KumikoPages

from .base_pages import AuctionItemSearchBasePages, OwnedAuctionItemBasePages
from .utils import (
    AuctionItem,
    AuctionItemCompactPageEntry,
    AuctionItemPageEntry,
    CompactAuctionItem,
    OwnedAuctionItem,
    OwnedAuctionItemPageEntry,
)


class AuctionPages(KumikoPages):
    def __init__(
        self, entries: List[AuctionItem], *, ctx: commands.Context, per_page: int = 1
    ):
        converted = [AuctionItemPageEntry(entry).to_dict() for entry in entries]
        super().__init__(EmbedListSource(converted, per_page=per_page), ctx=ctx)


class OwnedAuctionPages(OwnedAuctionItemBasePages):
    def __init__(
        self,
        entries: List[OwnedAuctionItem],
        *,
        ctx: commands.Context,
        per_page: int = 1,
        pool: asyncpg.Pool
    ):
        converted = [OwnedAuctionItemPageEntry(entry).to_dict() for entry in entries]
        super().__init__(converted, per_page=per_page, ctx=ctx, pool=pool)


class AuctionSearchPages(AuctionItemSearchBasePages):
    def __init__(
        self,
        entries: List[CompactAuctionItem],
        *,
        ctx: commands.Context,
        per_page: int = 10
    ):
        converted = [AuctionItemCompactPageEntry(entry) for entry in entries]
        super().__init__(converted, per_page=per_page, ctx=ctx)
