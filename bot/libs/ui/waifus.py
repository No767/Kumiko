from __future__ import annotations

from typing import TYPE_CHECKING, List

import ciso8601
import discord
import msgspec
from discord.utils import format_dt
from libs.utils.pages.paginator import KumikoPages
from libs.utils.pages.sources import EmbedListSource
from yarl import URL

if TYPE_CHECKING:
    from libs.utils.context import KContext


class NekosImages(msgspec.Struct):
    id: str
    tags: List[str]
    created_at: str


class NekosImageEntry:
    __slots__ = ("id", "tags", "created_at")

    def __init__(self, entry: NekosImages):
        self.id = entry.id
        self.tags = entry.tags
        self.created_at = entry.created_at

    def to_dict(self):
        base_url = URL("https://nekos.moe")
        full_image_url = base_url / "image" / self.id
        post_url = base_url / "post" / self.id
        desc = (
            f"**Post URL**: {str(post_url)}\n"
            f"**Image URL**: {str(full_image_url)}.jpg\n"
            f"**Created At**: {format_dt(ciso8601.parse_datetime(self.created_at))}\n"
            f"**Tags**: {', '.join(self.tags).rstrip(',')}"
        )
        data = {"description": desc, "image": str(full_image_url)}
        return data


class NekoImagesPages(KumikoPages):
    def __init__(self, entries: List[NekosImages], *, ctx: KContext, per_page: int = 1):
        converted = [NekosImageEntry(entry).to_dict() for entry in entries]
        super().__init__(EmbedListSource(converted, per_page=per_page), ctx=ctx)
        self.embed = discord.Embed(colour=discord.Colour.from_rgb(255, 125, 212))
