from __future__ import annotations

from typing import TYPE_CHECKING

import discord
from discord.app_commands import CommandTree

if TYPE_CHECKING:
    from bot.kumiko import Kumiko


class KumikoCommandTree(CommandTree):
    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        bot: Kumiko = interaction.client  # type: ignore # Checked and it is that
        if (
            bot.owner_id == interaction.user.id
            or bot.application_id == interaction.user.id
        ):
            return True

        # TODO - Add blacklist feature here.

        return True
