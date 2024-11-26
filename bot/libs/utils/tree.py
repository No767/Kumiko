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

        if interaction.user.id in bot.blacklist:
            msg = (
                f"My fellow user, {interaction.user.mention}, you just got the L. "
                "You are blacklisted from using this bot. Take an \U0001f1f1, \U0001f1f1oser. "
                "[Here is your appeal form](https://media.tenor.com/K9R9beOgPR4AAAAC/fortnite-thanos.gif)"
            )
            await interaction.response.send_message(msg, ephemeral=True)
            return False

        if interaction.guild and interaction.guild.id in bot.blacklist:
            await interaction.response.send_message(
                "This is so sad lolllllll! Your whole entire server got blacklisted!",
                ephemeral=True,
            )
            return False

        return True
