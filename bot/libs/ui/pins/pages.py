from typing import List, TypedDict

import discord
from discord.ext.commands import Context
from libs.utils.pages import KumikoPages, SimplePageSource


class SimplePages(KumikoPages):
    """A simple pagination session reminiscent of the old Pages interface.

    Basically an embed with some normal formatting.
    """

    def __init__(self, entries, *, ctx: Context, per_page: int = 12):
        super().__init__(SimplePageSource(entries, per_page=per_page), ctx=ctx)
        self.embed = discord.Embed(colour=discord.Colour.og_blurple())


class PinEntry(TypedDict):
    id: int
    name: str
    content: str


class PinPageEntry:
    __slots__ = ("id", "name")

    def __init__(self, entry: PinEntry):
        self.id: int = entry["id"]
        self.name: str = entry["name"]

    def __str__(self) -> str:
        return f"{self.name} (ID: {self.id})"


class PinPages(SimplePages):
    def __init__(self, entries: List[PinEntry], *, ctx: Context, per_page: int = 12):
        converted = [PinPageEntry(entry) for entry in entries]
        super().__init__(converted, per_page=per_page, ctx=ctx)
