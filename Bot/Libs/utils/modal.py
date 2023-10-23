from __future__ import annotations

from typing import TYPE_CHECKING

import discord
from discord.ext import commands

from .error_preset import produce_error_embed

if TYPE_CHECKING:
    from Bot.kumikocore import KumikoCore

NO_CONTROL_MSG = "This modal cannot be controlled by you, sorry!"


class KumikoModal(discord.ui.Modal):
    """Subclassed `discord.ui.Modal` that includes sane default functionality"""

    def __init__(self, ctx: commands.Context[KumikoCore], *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ctx = ctx

    async def interaction_check(self, interaction: discord.Interaction, /) -> bool:
        if interaction.user and interaction.user.id in (
            self.ctx.bot.application.owner.id,  # type: ignore
            self.ctx.author.id,
        ):
            return True
        await interaction.response.send_message(NO_CONTROL_MSG, ephemeral=True)
        return False

    async def on_error(
        self, interaction: discord.Interaction, error: Exception, /
    ) -> None:
        await interaction.response.send_message(
            embed=produce_error_embed(error), ephemeral=True
        )
        self.stop()
