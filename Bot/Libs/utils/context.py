from __future__ import annotations

from typing import TYPE_CHECKING, Optional

import discord
from discord.ext import commands

if TYPE_CHECKING:
    from Bot.kumikocore import KumikoCore

    from .view import KumikoView


class ConfirmationView(KumikoView):
    def __init__(self, ctx: KContext, timeout: float, delete_after: bool) -> None:
        super().__init__(ctx=ctx, display_message=False, timeout=timeout)
        self.value: Optional[bool] = None
        self.delete_after: bool = delete_after
        self.message: Optional[discord.Message] = None

    async def on_timeout(self) -> None:
        if self.message:
            if self.delete_after:
                await self.message.delete()
                return
            await self.message.edit(view=None)

    async def delete_response(self, interaction: discord.Interaction) -> None:
        await interaction.response.defer()
        await interaction.delete_original_response()
        self.stop()

    @discord.ui.button(
        label="Confirm",
        style=discord.ButtonStyle.green,
        emoji="<:greenTick:596576670815879169>",
    )
    async def confirm(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        self.value = True
        if self.delete_after:
            await self.delete_response(interaction)

    @discord.ui.button(
        label="Cancel",
        style=discord.ButtonStyle.red,
        emoji="<:redTick:596576672149667840>",
    )
    async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.value = False
        await self.delete_response(interaction)


class KContext(commands.Context):
    """Kumiko's custom `commands.Context` with extra features"""

    bot: KumikoCore

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.pool = self.bot.pool
        self.redis_pool = self.bot.redis_pool
        self.session = self.bot.session

    async def prompt(
        self, message: str, *, timeout: float = 60.0, delete_after: bool = True
    ) -> Optional[bool]:
        """Prompts the user with an interaction confirmation dialog

        Args:
            message (str): The message to show along with the prompt
            timeout (float, optional): How long to wait until returning. Defaults to 60.0.
            delete_after (bool, optional): Deletes the prompt afterwards. Defaults to True.
            author_id (Optional[int], optional): The member who should respond to the prompt. Defaults to the author.

        Returns:
            Optional[bool]: The response of the prompt

            - ``True`` if explicit confirm,

            - ``False`` if explicit deny,

            - ``None`` if deny due to timeout
        """
        view = ConfirmationView(self, timeout, delete_after)
        view.message = await self.send(message, view=view, ephemeral=delete_after)
        await view.wait()
        return view.value


class GuildContext(KContext):
    author: discord.Member
    guild: discord.Guild
