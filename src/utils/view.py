from typing import Any, Optional

import discord

from .context import KumikoContext
from .embeds import ErrorEmbed, FullErrorEmbed

NO_CONTROL_MSG = "This view cannot be controlled by you, sorry!"


class KumikoView(discord.ui.View):
    """Subclassed `discord.ui.View` that includes sane default configs"""

    def __init__(
        self, ctx: KumikoContext, *, view_timeout: Optional[float] = 180
    ) -> None:
        super().__init__(timeout=view_timeout)
        self.ctx = ctx
        self.message: Optional[discord.Message]

    async def interaction_check(self, interaction: discord.Interaction, /) -> bool:
        if interaction.user and interaction.user.id in (
            self.ctx.bot.application.owner.id,  # type: ignore
            self.ctx.author.id,
        ):
            return True
        await interaction.response.send_message(NO_CONTROL_MSG, ephemeral=True)
        return False

    async def on_error(
        self,
        interaction: discord.Interaction,
        error: Exception,
        item: discord.ui.Item[Any],
        /,
    ) -> None:
        self.ctx.bot.logger.exception(
            "Ignoring view exception from %s: ",
            self.__class__.__name__,
            exc_info=error,
        )
        await interaction.response.send_message(
            embed=FullErrorEmbed(error), ephemeral=True
        )
        self.stop()

    async def on_timeout(self) -> None:
        # This is the only way you can really edit the original message
        if self.message:
            embed = ErrorEmbed()
            embed.title = "\U00002757 Timed Out"
            embed.description = "Timed out waiting for a response. Cancelling action..."
            await self.message.edit(embed=embed, view=None)


class ConfirmationView(KumikoView):
    def __init__(
        self, ctx: KumikoContext, timeout: float, *, delete_after: bool
    ) -> None:
        super().__init__(ctx, timeout=timeout)
        self.value: Optional[bool]
        self.delete_after = delete_after
        self.message: Optional[discord.Message]

    async def on_timeout(self) -> None:
        if self.delete_after and self.message:
            await self.message.delete()
        elif self.message:
            await self.message.edit(view=None)

    async def delete_response(self, interaction: discord.Interaction) -> None:
        await interaction.response.defer()
        if self.delete_after:
            await interaction.delete_original_response()

        self.stop()

    @discord.ui.button(
        label="Confirm",
        style=discord.ButtonStyle.green,
        emoji="<:greenTick:596576670815879169>",
    )
    async def confirm(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ) -> None:
        self.value = True
        await self.delete_response(interaction)

    @discord.ui.button(
        label="Cancel",
        style=discord.ButtonStyle.red,
        emoji="<:redTick:596576672149667840>",
    )
    async def cancel(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ) -> None:
        self.value = False
        await interaction.response.defer()
        await interaction.delete_original_response()
        self.stop()
