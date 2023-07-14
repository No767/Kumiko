from discord import PartialEmoji, app_commands
from discord.ext import commands
from discord.utils import format_dt, utcnow
from kumikocore import KumikoCore
from Libs.cog_utils.pins import formatOptions, getPinInfo, getPinText
from Libs.ui.pins import CreatePin
from Libs.utils import Embed


class Pins(commands.Cog):
    """Pin text for later retrieval"""

    def __init__(self, bot: KumikoCore):
        self.bot = bot
        self.pool = self.bot.pool

    @property
    def display_emoji(self) -> PartialEmoji:
        return PartialEmoji(name="\U0001f4cc")

    @commands.hybrid_group(name="pins", fallback="get")
    @app_commands.describe(name="Pin to get")
    async def pins(self, ctx: commands.Context, *, name: str):
        """Pin text for later retrieval"""
        pinText = await getPinText(ctx.guild.id, name, self.bot.pool)
        if pinText is None or isinstance(pinText, str) is False:
            await ctx.send(formatOptions(pinText))
            return
        await ctx.send(pinText)

    @pins.command(name="create")
    async def createPin(self, ctx: commands.Context) -> None:
        """Create a pin"""
        createPinModal = CreatePin(self.pool)
        await ctx.interaction.response.send_modal(createPinModal)

    @pins.command(name="info")
    @app_commands.describe(name="Pin name to search")
    async def pinInfo(self, ctx: commands.Context, name: str) -> None:
        """Provides info about a pin"""
        pinInfo = await getPinInfo(ctx.guild.id, name, self.pool)
        if pinInfo is None:
            await ctx.send("Pin not found.")
            return
        embed = Embed()
        embed.title = pinInfo["name"]
        embed.timestamp = utcnow()
        embed.add_field(name="Owner", value=f"<@{pinInfo['author_id']}>")
        embed.add_field(name="Created At", value=format_dt(pinInfo["created_at"]))
        await ctx.send(embed=embed)


async def setup(bot: KumikoCore):
    await bot.add_cog(Pins(bot))
