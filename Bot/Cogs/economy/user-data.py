import discord
from discord.ext import commands
from discord.commands import slash_command, Option
import asyncio
import uvloop
from eco_base_sql import kumikoEcoUtils



class EcoV1(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(name="balance", description="Gets user balance", guild_ids=[866199405090308116])
    async def ecoBal(self, ctx):
        eco = kumikoEcoUtils(ctx)
        user = ctx.author
