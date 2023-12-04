from __future__ import annotations

from typing import TYPE_CHECKING, Any, Optional

import discord

from .embeds import ErrorEmbed
from .utils import produce_error_embed

if TYPE_CHECKING:
    from .context import KContext

NO_CONTROL_MSG = "This view cannot be controlled by you, sorry!"


class KumikoView(discord.ui.View):
    """Subclassed `discord.ui.View` that includes sane default functionality"""

    def __init__(self, ctx: KContext, display_message: bool = True, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ctx = ctx
        self.message: Optional[discord.Message] = None
        self.display_message = display_message

    async def interaction_check(self, interaction: discord.Interaction, /) -> bool:
        if interaction.user and interaction.user.id in (
            self.ctx.bot.application.owner.id,  # type: ignore
            self.ctx.author.id,
        ):
            return True

        await interaction.response.send_message(NO_CONTROL_MSG, ephemeral=True)
        return False

    async def on_timeout(self) -> None:
        if self.message:
            if self.display_message:
                embed = ErrorEmbed()
                embed.title = "\U00002757 Timed Out"
                embed.description = (
                    "Timed out waiting for a response. Cancelling action..."
                )
                await self.message.edit(embed=embed, view=None)
                return

            await self.message.edit(view=None)

    async def on_error(
        self,
        interaction: discord.Interaction,
        error: Exception,
        item: discord.ui.Item[Any],
        /,
    ) -> None:
        await interaction.response.send_message(
            embed=produce_error_embed(error), ephemeral=True
        )
        self.stop()
