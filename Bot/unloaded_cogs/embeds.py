from Libs.utils import Embed
from discord.ext import commands
from kumikocore import KumikoCore
import logging
from discord.utils import utcnow
class EmbedCog(commands.Cog):
    """Embed test cog - Please only sync locally"""
    def __init__(self, bot: KumikoCore) -> None:
        self.bot = bot
        self.logger = logging.getLogger("discord")

    @commands.hybrid_command(name="embed-time")
    async def embedTime(self, ctx: commands.Context) -> None:
        embed = Embed()
        embed.timestamp = utcnow()
        self.logger.info(f"Timestamp: {embed.timestamp}")
        embed.set_footer(text=f"{embed.timestamp}")
        await ctx.send(embed=embed)

async def setup(bot: KumikoCore) -> None:
    await bot.add_cog(EmbedCog(bot))
