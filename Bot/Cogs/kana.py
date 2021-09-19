import pykakasi
import tensorflow as tf
from discord import Embed
from discord.ext import commands


class kana(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="kanatranslate")
    async def kanatranslate(self, ctx, search: str):
        kks = pykakasi.kakasi()
        kks.setMode("H", "a")
