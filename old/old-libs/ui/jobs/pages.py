from typing import List, TypedDict

import discord
from discord.ext.commands import Context
from Libs.utils.pages import KumikoPages, SimplePageSource


class SimplePages(KumikoPages):
    """A simple pagination session reminiscent of the old Pages interface.

    Basically an embed with some normal formatting.
    """

    def __init__(self, entries, *, ctx: Context, per_page: int = 12):
        super().__init__(SimplePageSource(entries, per_page=per_page), ctx=ctx)
        self.embed = discord.Embed(colour=discord.Colour.og_blurple())


class JobEntry(TypedDict):
    id: int
    name: str
    description: str
    required_rank: int
    pay_amount: int


class JobPageEntry:
    __slots__ = ("id", "name", "description", "required_rank", "pay_amount")

    def __init__(self, entry: JobEntry):
        self.id: int = entry["id"]
        self.name: str = entry["name"]
        self.description: str = entry["description"]
        self.required_rank: int = entry["required_rank"]
        self.pay_amount: int = entry["pay_amount"]

    def __str__(self) -> str:
        return f"(ID: {self.id}) {self.name} (RR: {self.required_rank} | Pay: {self.pay_amount})"


class JobPages(SimplePages):
    def __init__(self, entries: List[JobEntry], *, ctx: Context, per_page: int = 10):
        converted = [JobPageEntry(entry) for entry in entries]
        super().__init__(converted, per_page=per_page, ctx=ctx)
