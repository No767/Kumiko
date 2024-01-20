import discord
from discord.ext import commands
from kumikocore import KumikoCore


class VoiceSummary(commands.Cog):
    def __init__(self, bot: KumikoCore) -> None:
        self.bot = bot

    @property
    def display_emoji(self) -> discord.PartialEmoji:
        return discord.PartialEmoji.from_str("<:upward_stonks:739614245997641740>")

    @property
    def configurable(self) -> bool:
        return True


async def setup(bot: KumikoCore) -> None:
    await bot.add_cog(VoiceSummary(bot))
