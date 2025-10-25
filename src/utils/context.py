from __future__ import annotations

from typing import TYPE_CHECKING, Optional

import discord
from discord.ext import commands

from .view import KumikoView

if TYPE_CHECKING:
    from core import Kumiko
    from utils.context import KumikoContext

NO_CONTROL_MSG = "This view cannot be controlled by you, sorry!"


# Why not subclass KumikoView?
# It results in a circular logic, so instead
# we subclassed discord.ui.View and pretty much implement what KumikoView does anyways
class ConfirmationView(KumikoView):
    def __init__(self, ctx: KumikoContext, timeout: float, *, delete_after: bool):
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


class KumikoContext(commands.Context):
    """Kumiko's custom `commands.Context` with extra features"""

    bot: Kumiko

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.pool = self.bot.pool
        self.session = self.bot.session

    async def prompt(
        self, message: str, *, prompt_timeout: float = 60.0, delete_after: bool = True
    ) -> Optional[bool]:
        """Prompts the user with an interaction confirmation dialog

        Args:
            message (str): The message to show along with the prompt
            prompt_timeout (float, optional): How long to wait until returning. Defaults to 60.0.
            delete_after (bool, optional): Deletes the prompt afterwards. Defaults to True.
            author_id (Optional[int], optional): The member who should respond to the prompt. Defaults to the author.

        Returns:
            Optional[bool]: The response of the prompt

            - ``True`` if explicit confirm,

            - ``False`` if explicit deny,

            - ``None`` if deny due to prompt_timeout
        """
        view = ConfirmationView(self, prompt_timeout, delete_after)
        view.message = await self.send(message, view=view, ephemeral=delete_after)
        await view.wait()
        return view.value

    async def get_or_fetch_member(
        self, guild: discord.Guild, member_id: int
    ) -> Optional[discord.Member]:
        """Gets or fetches a member from the guild

        Args:
            guild (discord.Guild): Guild Object
            member_id (int): The ID of the member

        Returns:
            Optional[discord.Member]: An `discord.Member` if found, `None` if not found.
        """
        member = guild.get_member(member_id)
        if member is not None:
            return member
        members = await guild.query_members(limit=1, user_ids=[member_id], cache=True)
        if not members:
            return None
        return members[0]


class GuildContext(KumikoContext):
    """An `KumikoContext` that represents a context found in a guild command"""

    # This is in fact correct
    author: discord.Member  # type: ignore
    guild: discord.Guild  # type: ignore
