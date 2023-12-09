import sys
from pathlib import Path

path = Path(__file__).parents[3].joinpath("Bot")
sys.path.append(str(path))

from discord.ext import commands
from Libs.cog_utils.moderation import TimeoutDTConverter


class ModCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="modconvert")
    async def modconvert(self, ctx, *, duration: TimeoutDTConverter):
        await ctx.send(f"{duration}")


async def setup(bot):
    await bot.add_cog(ModCog(bot))
