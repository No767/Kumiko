from typing import Any

import discord
from discord.ext import commands

from .utils import make_error_embed

NO_CONTROL_MSG = "This view cannot be controlled by you, sorry!"


class KumikoView(discord.ui.View):
    def __init__(self, ctx: commands.Context):
        super().__init__()
        self.ctx = ctx

    async def interaction_check(self, interaction: discord.Interaction, /) -> bool:
        if interaction.user and interaction.user in (
            self.ctx.bot.application.owner.id,  # type: ignore,
            self.ctx.author.id,
        ):
            return True

        await interaction.response.send_message(NO_CONTROL_MSG, ephemeral=True)
        return False

    async def on_timeout(self) -> None:
        self.clear_items()
        self.stop()

    async def on_error(
        self,
        interaction: discord.Interaction,
        error: Exception,
        item: discord.ui.Item[Any],
        /,
    ) -> None:
        await interaction.response.send_message(
            embed=make_error_embed(error), ephemeral=True
        )
        self.stop()
