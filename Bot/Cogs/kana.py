from discord.ext import commands
from discord import Embed
import pykakasi
import tensorflow as tf


class kana(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="kanatranslate")
    async def kanatranslate (self, ctx, search:str):
        kks = pykakasi.kakasi()
        kks.setMode("H", "a")



