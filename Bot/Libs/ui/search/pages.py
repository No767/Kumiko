from typing import List

from discord.ext import commands
from Libs.utils.pages import EmbedListSource, KumikoPages

from .page_entries import ModrinthProjectEntry
from .structs import ModrinthProject


class ModrinthPages(KumikoPages):
    def __init__(self, entries: List[ModrinthProject], *, ctx: commands.Context):
        converted = [ModrinthProjectEntry(entry).to_dict() for entry in entries]
        super().__init__(EmbedListSource(converted, per_page=1), ctx=ctx)
