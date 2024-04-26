from typing import Dict


class BlacklistPageEntry:
    __slots__ = "entry"

    def __init__(self, entry: Dict[int, bool]):
        self.entry = entry

    def __str__(self) -> str:
        value = list(self.entry.values())[0]
        bl_status = "Blacklisted" if value is True else "None"
        return f"{list(self.entry.keys())[0]}: (Bool Status: {value} | Status: {bl_status})"
