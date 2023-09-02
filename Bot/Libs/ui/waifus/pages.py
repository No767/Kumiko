from typing import List

import discord
from discord.ext import commands
from Libs.utils.pages import EmbedListSource, KumikoPages

from .structs import NekosImages
from .utils import NekosImageEntry


class NekoImagesPages(KumikoPages):
    def __init__(
        self, entries: List[NekosImages], *, ctx: commands.Context, per_page: int = 1
    ):
        converted = [NekosImageEntry(entry).to_dict() for entry in entries]
        super().__init__(EmbedListSource(converted, per_page=per_page), ctx=ctx)
        self.embed = discord.Embed(colour=discord.Colour.from_rgb(255, 125, 212))
