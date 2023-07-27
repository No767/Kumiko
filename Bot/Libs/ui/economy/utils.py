from typing import TypedDict


class LeaderboardEntry(TypedDict):
    id: int
    rank: int
    petals: int


class LeaderboardPageEntry:
    __slots__ = ("id", "rank", "petals")

    def __init__(self, entry: LeaderboardEntry):
        self.id = entry["id"]
        self.rank = entry["rank"]
        self.petals = entry["petals"]

    def __str__(self) -> str:
        return f"<@{self.id}>: {self.petals} 🌸 | (Rank: {self.rank})"
