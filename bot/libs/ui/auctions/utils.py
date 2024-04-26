import datetime
from typing import Any, Dict, TypedDict

from discord.utils import format_dt


class AuctionItem(TypedDict):
    id: int
    name: str
    description: str
    user_id: int
    amount_listed: int
    listed_price: int
    listed_at: datetime.datetime


class CompactAuctionItem(TypedDict):
    item_id: int
    item_name: str
    user_id: int
    amount_listed: int


class OwnedAuctionItem(TypedDict):
    id: int
    name: str
    description: str
    amount_listed: int
    listed_price: int
    listed_at: datetime.datetime


class AuctionItemPageEntry:
    __slots__ = (
        "id",
        "name",
        "description",
        "user_id",
        "amount_listed",
        "listed_price",
        "listed_at",
    )

    def __init__(self, entry: AuctionItem):
        self.id = entry["id"]
        self.name = entry["name"]
        self.description = entry["description"]
        self.user_id = entry["user_id"]
        self.amount_listed = entry["amount_listed"]
        self.listed_price = entry["listed_price"]
        self.listed_at = entry["listed_at"]

    def to_dict(self) -> Dict[str, Any]:
        data = {
            "title": self.name,
            "description": self.description,
            "fields": [
                {"name": "Price", "value": self.listed_price, "inline": True},
                {"name": "Amount Listed", "value": self.amount_listed, "inline": True},
                {"name": "Listed By", "value": f"<@{self.user_id}>", "inline": True},
                {"name": "ID", "value": self.id, "inline": True},
                {
                    "name": "Listed At",
                    "value": format_dt(
                        self.listed_at.replace(tzinfo=datetime.timezone.utc)
                    ),
                    "inline": True,
                },
            ],
        }
        return data


class AuctionItemCompactPageEntry:
    __slots__ = ("item_id", "item_name", "user_id", "amount_listed")

    def __init__(self, entry: CompactAuctionItem):
        self.item_id = entry["item_id"]
        self.item_name = entry["item_name"]
        self.user_id = entry["user_id"]
        self.amount_listed = entry["amount_listed"]

    def __str__(self) -> str:
        return f"{self.item_name} | (ID: {self.item_id}) (Amt: {self.amount_listed}) (Listed By: <@{self.user_id}>)"


class OwnedAuctionItemPageEntry:
    __slots__ = (
        "id",
        "name",
        "desc",
        "user_id",
        "amount_listed",
        "listed_price",
        "listed_at",
    )

    def __init__(self, entry: OwnedAuctionItem):
        self.id = entry["id"]
        self.name = entry["name"]
        self.desc = entry["description"]
        self.amount_listed = entry["amount_listed"]
        self.listed_price = entry["listed_price"]
        self.listed_at = entry["listed_at"]

    def to_dict(self) -> Dict[str, Any]:
        data = {
            "title": self.name,
            "description": self.desc,
            "fields": [
                {"name": "Price", "value": self.listed_price, "inline": True},
                {"name": "Amount Listed", "value": self.amount_listed, "inline": True},
                {
                    "name": "Listed At",
                    "value": format_dt(
                        self.listed_at.replace(tzinfo=datetime.timezone.utc)
                    ),
                    "inline": True,
                },
                {"name": "ID", "value": self.id, "inline": True},
            ],
        }
        return data
