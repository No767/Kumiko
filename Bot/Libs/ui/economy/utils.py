from typing import Any, Dict, TypedDict


class LeaderboardEntry(TypedDict):
    id: int
    rank: int
    petals: int


class UserInvEntry(TypedDict):
    id: int
    name: str
    description: str
    price: int
    amount: int
    producer_id: int


class LeaderboardPageEntry:
    __slots__ = ("id", "rank", "petals")

    def __init__(self, entry: LeaderboardEntry):
        self.id = entry["id"]
        self.rank = entry["rank"]
        self.petals = entry["petals"]

    def __str__(self) -> str:
        return f"<@{self.id}>: {self.petals} 🌸 | (Rank: {self.rank})"


class UserInvPageEntry:
    __slots__ = ("id", "name", "description", "price", "amount")

    def __init__(self, entries: UserInvEntry):
        self.id: int = entries["id"]
        self.name: str = entries["name"]
        self.description: str = entries["description"]
        self.price: int = entries["price"]
        self.amount: int = entries["amount"]

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
