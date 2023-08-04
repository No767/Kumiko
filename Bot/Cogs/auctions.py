from discord import PartialEmoji
from discord.ext import commands
from kumikocore import KumikoCore


class Auctions(commands.Cog):
    """List unwanted items away here"""

    def __init__(self, bot: KumikoCore) -> None:
        self.bot = bot

    @property
    def display_emoji(self) -> PartialEmoji:
        return PartialEmoji.from_str("<:auction_house:1136906394323398749>")

    @commands.hybrid_group(
        name="auctions", fallback="view", aliases=["auction-house", "ah"]
    )
    async def auctions(self, ctx: commands.Context) -> None:
        """List the items available for purchase"""

    @auctions.command(name="list", aliases=["ls"])
    async def list_auctions(self, ctx: commands.Context) -> None:
        """List the items available for purchase"""


async def setup(bot: KumikoCore) -> None:
    await bot.add_cog(Auctions(bot))
