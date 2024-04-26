from .structs import SimplePrideProfileEntry, SimpleViewsEntry


class SimplePrideProfilesPageEntry:
    __slots__ = ("id", "name", "pronouns")

    def __init__(self, entry: SimplePrideProfileEntry):
        self.id = entry["id"]
        self.name = entry["name"]
        self.pronouns = entry["pronouns"]

    def __str__(self) -> str:
        return f"{self.name} (<@{self.id}> | {self.pronouns or 'None'})"


class ViewsPrideProfilesPageEntry:
    __slots__ = ("id", "name", "views")

    def __init__(self, entry: SimpleViewsEntry):
        self.id = entry["id"]
        self.name = entry["name"]
        self.views = entry["views"]

    def __str__(self) -> str:
        return f"{self.name} (<@{self.id}> | {self.views} view(s))"
