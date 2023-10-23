from __future__ import annotations

from typing import TYPE_CHECKING

import discord
from discord.app_commands import CommandTree

from .blacklist import get_or_fetch_blacklist
from .message_constants import MessageConstants

if TYPE_CHECKING:
    from Bot.kumikocore import KumikoCore


class KumikoCommandTree(CommandTree):
    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        bot: KumikoCore = interaction.client  # type: ignore # Pretty much returns the subclass anyways. I checked - Noelle
        if (
            bot.owner_id == interaction.user.id
            or bot.application_id == interaction.user.id
        ):
            return True

        blacklisted_status = await get_or_fetch_blacklist(
            bot, interaction.user.id, bot.pool
        )
        if blacklisted_status is True:
            # Get RickRolled lol
            # While implementing this, I was listening to Rick Astley
            await interaction.response.send_message(
                f"My fellow user, {interaction.user.mention}, you just got the L. {MessageConstants.BLACKLIST_APPEAL_MSG.value}",
                suppress_embeds=True,
            )
            return False
        return True
