from typing import List

from discord.ext import commands
from Libs.utils.pages import EmbedListSource, KumikoPages

from .page_entries import (
    AniListAnimeEntry,
    AniListMangaEntry,
    ModrinthProjectEntry,
)
from .structs import AniListAnime, AniListManga, ModrinthProject


class ModrinthPages(KumikoPages):
    def __init__(self, entries: List[ModrinthProject], *, ctx: commands.Context):
        converted = [ModrinthProjectEntry(entry).to_dict() for entry in entries]
        super().__init__(EmbedListSource(converted, per_page=1), ctx=ctx)


class AniListMangaPages(KumikoPages):
    def __init__(self, entries: List[AniListManga], *, ctx: commands.Context):
        converted = [AniListMangaEntry(entry).to_dict() for entry in entries]
        super().__init__(EmbedListSource(converted, per_page=1), ctx=ctx)


class AniListAnimePages(KumikoPages):
    def __init__(self, entries: List[AniListAnime], *, ctx: commands.Context):
        converted = [AniListAnimeEntry(entry).to_dict() for entry in entries]
        super().__init__(EmbedListSource(converted, per_page=1), ctx=ctx)
