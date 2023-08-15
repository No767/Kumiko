from typing import Any, Dict, List, TypedDict

import discord
from discord.ext.commands import Context
from Libs.utils.pages import EmbedListSource, KumikoPages, SimplePageSource


class SimpleItemPages(KumikoPages):
    def __init__(self, entries, *, ctx: Context, per_page: int = 1):
        super().__init__(EmbedListSource(entries, per_page=per_page), ctx=ctx)
        self.embed = discord.Embed(colour=discord.Colour.og_blurple())


class ItemEntry(TypedDict):
    id: int
    name: str
    description: str
    price: int
    amount: int
    producer_id: int


class ItemPageEntry:
    __slots__ = ("id", "name", "description", "price", "amount")

    def __init__(self, entries: ItemEntry):
        self.id: int = entries["id"]
        self.name: str = entries["name"]
        self.description: str = entries["description"]
        self.price: int = entries["price"]
        self.amount: int = entries["amount"]

    def to_embed(self) -> discord.Embed:
        embed = discord.Embed()
        embed.title = self.name
        embed.description = self.description
        embed.add_field(name="ID", value=self.id)
        embed.add_field(name="Price", value=self.price)
        embed.add_field(name="Amount", value=self.amount)
        return embed

    def to_dict(self) -> Dict[str, Any]:
        data = {
            "title": self.name,
            "description": self.description,
            "fields": [
                {"name": "ID", "value": self.id, "inline": True},
                {"name": "Price", "value": self.price, "inline": True},
                {"name": "Amount", "value": self.amount, "inline": True},
            ],
        }
        return data


class ItemPages(SimpleItemPages):
    def __init__(self, entries: List[ItemEntry], *, ctx: Context, per_page: int = 1):
        converted = [ItemPageEntry(entry).to_dict() for entry in entries]
        super().__init__(converted, per_page=per_page, ctx=ctx)


class SimplePages(KumikoPages):
    """A simple pagination session reminiscent of the old Pages interface.

    Basically an embed with some normal formatting.
    """

    def __init__(self, entries, *, ctx: Context, per_page: int = 12):
        super().__init__(SimplePageSource(entries, per_page=per_page), ctx=ctx)
        self.embed = discord.Embed(colour=discord.Colour.og_blurple())


class SimpleItemEntry(TypedDict):
    id: int
    name: str


class SimpleItemPageEntry:
    __slots__ = ("id", "name")

    def __init__(self, entry: SimpleItemEntry):
        self.id: int = entry["id"]
        self.name: str = entry["name"]

    def __str__(self) -> str:
        return f"{self.name} (ID: {self.id})"


class SimpleSearchItemPages(SimplePages):
    def __init__(
        self, entries: List[SimpleItemEntry], *, ctx: Context, per_page: int = 12
    ):
        converted = [SimpleItemPageEntry(entry) for entry in entries]
        super().__init__(converted, per_page=per_page, ctx=ctx)
