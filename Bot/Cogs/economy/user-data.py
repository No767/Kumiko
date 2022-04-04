
from discord.commands import slash_command
from discord.ext import commands
from eco_base_sql import kumikoEcoUtils


class EcoV1(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(
        name="balance", description="Gets user balance", guild_ids=[866199405090308116]
    )
    async def ecoBal(self, ctx):
        kumikoEcoUtils(ctx)
        ctx.author
