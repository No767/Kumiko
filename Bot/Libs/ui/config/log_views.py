from __future__ import annotations

from typing import TYPE_CHECKING

import discord
from discord.ext import commands
from Libs.config.cache import GuildCacheHandler, LoggingGuildConfig
from Libs.utils import KumikoView

if TYPE_CHECKING:
    from Bot.Cogs.config import Config
    from Bot.kumikocore import KumikoCore


class LoggingConfigMenu(discord.ui.Select):
    def __init__(self, cog: Config, ctx: commands.Context) -> None:
        options = [
            discord.SelectOption(
                emoji=discord.PartialEmoji.from_str("<:blobban:759935431847968788>"),
                label="Moderation",
                description="Enabled/Disable Moderation Logs",
                value="mod",
            ),
            discord.SelectOption(
                emoji=discord.PartialEmoji.from_str(
                    "<:upward_stonks:739614245997641740>"
                ),
                label="Economy",
                description="Enable/Disable Local Economy Logs",
                value="eco",
            ),
            discord.SelectOption(
                emoji=discord.PartialEmoji(name="\U0001f500"),
                label="Redirects",
                description="Enable/Disable Redirects Logs",
                value="redirects",
            ),
        ]
        super().__init__(placeholder="Select a category...", options=options, row=0)
        self.cog = cog
        self.ctx = ctx

    async def callback(self, interaction: discord.Interaction) -> None:
        value = self.values[0]
        view = LGCToggleView(self.cog, self.ctx, value)
        await interaction.response.send_message(f"You selected: {value}", view=view)


class LGCView(KumikoView):
    def __init__(self, bot: KumikoCore, cog: Config, ctx: commands.Context) -> None:
        super().__init__(ctx)
        self.conf_cog = cog
        self.bot = bot
        self.pool = self.bot.pool
        self.redis_pool = self.bot.redis_pool
        self.add_item(LoggingConfigMenu(cog, ctx))

    @discord.ui.button(label="Save and Finish", style=discord.ButtonStyle.green, row=1)
    async def save_and_finish(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ) -> None:
        query = """
        UPDATE logging_config
        SET mod = $2,
            eco = $3,
            redirects = $4
        WHERE guild_id = $1;
        """
        if interaction.guild is None:
            return

        cache = GuildCacheHandler(interaction.guild.id, self.redis_pool)
        cached_status = self.conf_cog.get_cached_lgc(interaction.guild.id)
        if cached_status is None:
            return

        new_conf = LoggingGuildConfig(**cached_status)
        status_values = [v for v in cached_status.values()]
        await self.pool.execute(query, interaction.guild.id, *status_values)
        await cache.replace_config(".logging_config", new_conf)
        self.conf_cog.remove_lgc(interaction.guild.id)
        await interaction.response.defer()
        await interaction.delete_original_response()
        self.stop()


class LGCToggleView(KumikoView):
    def __init__(self, cog: Config, ctx: commands.Context, value: str) -> None:
        super().__init__(ctx)
        self.ctx = ctx
        self.conf_cog = cog
        self.value = value

    async def set_status(self, interaction: discord.Interaction, status: bool):
        str_status = "enabled" if status is True else "disabled"

        if interaction.guild is None or self.conf_cog is None:
            return

        is_already_enabled = self.conf_cog.check_lgc_value_enabled(
            interaction.guild.id, self.value
        )
        if is_already_enabled is status:
            await interaction.response.send_message(
                f"Module `{self.value} is already {str_status}!`", ephemeral=True
            )
            return

        if self.conf_cog.is_lgc_in(interaction.guild.id):
            self.conf_cog.set_lgc(interaction.guild.id, self.value, status)
            await interaction.response.send_message(
                f"Module `{self.value}` is now {str_status}", ephemeral=True
            )
            return

        await interaction.response.send_message("You did not start the config progress")

    @discord.ui.button(
        label="Enable",
        style=discord.ButtonStyle.green,
        emoji="<:greenTick:596576670815879169>",
        row=0,
    )
    async def enable(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ) -> None:
        await self.set_status(interaction, True)

    @discord.ui.button(
        label="Disable",
        style=discord.ButtonStyle.red,
        emoji="<:redTick:596576672149667840>",
        row=0,
    )
    async def disable(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ) -> None:
        await self.set_status(interaction, False)

    @discord.ui.button(
        label="Finish",
        style=discord.ButtonStyle.grey,
    )
    async def finish(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ) -> None:
        await interaction.response.defer()
        await interaction.delete_original_response()
        self.stop()
