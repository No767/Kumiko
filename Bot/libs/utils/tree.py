from __future__ import annotations

from typing import TYPE_CHECKING

import discord
from discord.app_commands import CommandTree

from .message_constants import MessageConstants

if TYPE_CHECKING:
    from Bot.kumikocore import KumikoCore

    from .blacklist import get_blacklist


class KumikoCommandTree(CommandTree):
    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        bot: KumikoCore = interaction.client  # type: ignore # Checked and it is that
        user = interaction.user
        if bot.owner_id == user.id or bot.application_id == user.id:
            return True

        blacklist = await get_blacklist(user.id)

        if blacklist is not None:
            await interaction.response.send_message(
                f"My fellow user, {user.mention}, you just got the L. {MessageConstants.BLACKLIST_APPEAL_MSG.value}",
                suppress_embeds=True,
            )
            return False
        return True
