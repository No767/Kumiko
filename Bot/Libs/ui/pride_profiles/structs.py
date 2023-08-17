from typing import TypedDict


class SimplePrideProfileEntry(TypedDict):
    id: int
    name: str
    pronouns: str


class SimpleViewsEntry(TypedDict):
    id: int
    name: str
    views: int
