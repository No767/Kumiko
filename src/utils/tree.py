from __future__ import annotations

from typing import TYPE_CHECKING

from discord.app_commands import CommandTree

if TYPE_CHECKING:
    import discord

    from core import Kumiko


class KumikoCommandTree(CommandTree):
    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        bot: Kumiko = interaction.client  # type: ignore # Checked and it is that
        if interaction.user.id in (bot.owner_id, bot.application_id):
            return True

        if interaction.user.id in bot.blacklist:
            bot.metrics.blacklist.commands.inc(1)
            msg = (
                f"My fellow user, {interaction.user.mention}, you just got the L. "
                "You are blacklisted from using this bot. Take an \U0001f1f1, \U0001f1f1oser. "
                "[Here is your appeal form](https://media.tenor.com/K9R9beOgPR4AAAAC/fortnite-thanos.gif)"
            )
            await interaction.response.send_message(msg, ephemeral=True)
            return False

        if interaction.guild and interaction.guild.id in bot.blacklist:
            bot.metrics.blacklist.commands.inc(1)
            await interaction.response.send_message(
                "This is so sad lolllllll! Your whole entire server got blacklisted!",
                ephemeral=True,
            )
            return False

        bot.metrics.commands.invocation.inc()
        if interaction.command:
            name = interaction.command.qualified_name
            bot.metrics.commands.count.labels(name).inc()

        return True
