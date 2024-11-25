from __future__ import annotations

from typing import TYPE_CHECKING

import discord
from libs.config import GuildCacheHandler, GuildConfig
from libs.utils import Embed, KumikoView

from .utils import determine_status, format_conf_desc

if TYPE_CHECKING:
    from libs.utils.context import KContext

    from bot.cogs.config import Config
    from bot.kumiko import KumikoCore


class ConfigMenu(discord.ui.Select):
    def __init__(self, bot: KumikoCore, ctx: KContext, config_cog: Config) -> None:
        self.bot = bot
        self.ctx = ctx
        self.config_cog = config_cog
        options = [
            discord.SelectOption(
                emoji=getattr(cog, "display_emoji", None),
                label=cog_name,
                description=cog.__doc__.split("\n")[0]
                if cog.__doc__ is not None
                else None,
                value=cog_name,
            )
            for cog_name, cog in self.bot.cogs.items()
            if getattr(cog, "configurable", None) is not None
        ]
        super().__init__(placeholder="Select a category...", options=options, row=0)

    async def callback(self, interaction: discord.Interaction) -> None:
        # I know that this is pretty dirty on how to do it, but there is quite literally no other way to do it
        # You can't just define a variable for columns
        # See https://github.com/MagicStack/asyncpg/issues/208#issuecomment-335498184
        assert interaction.guild is not None
        value = self.values[0]
        value_to_key = {
            "Economy": "local_economy",
            "Redirects": "redirects",
            "EventsLog": "logs",
            "Pins": "pins",
        }
        key = value_to_key[value]
        current_status = self.config_cog.reserved_configs[interaction.guild.id][key]
        view = ToggleCacheView(self.ctx, self.config_cog, value)
        embed = Embed()
        embed.description = format_conf_desc(value, current_status)
        await interaction.response.send_message(embed=embed, view=view)

        view.original_response = await interaction.original_response()  # type: ignore


class ToggleCacheView(KumikoView):
    def __init__(self, ctx: KContext, config_cog: Config, value: str):
        super().__init__(ctx)
        self.ctx = ctx
        self.config_cog = config_cog
        self.value = value

    async def set_cached_status(
        self,
        interaction: discord.Interaction,
        original_resp: discord.InteractionMessage,
        status: bool,
    ) -> None:
        value_to_key = {
            "Economy": "local_economy",
            "Redirects": "redirects",
            "EventsLog": "logs",
            "Pins": "pins",
        }
        key = value_to_key[self.value]
        str_status = determine_status(status)
        if interaction.guild is None or self.config_cog is None:
            return

        guild_id = interaction.guild.id
        is_already_enabled = self.config_cog.is_config_already_enabled(
            guild_id, self.value
        )
        if is_already_enabled is status:
            await interaction.response.send_message(
                f"Module `{self.value}` is already {str_status.lower()}!",
                ephemeral=True,
            )
            return

        # This will only run if the module is enabled/disabled
        if guild_id in self.config_cog.reserved_configs:
            self.config_cog.reserved_configs[guild_id][key] = status
            await original_resp.edit(
                embed=Embed(description=format_conf_desc(self.value, status))
            )
            await interaction.response.send_message(
                f"Module `{self.value}` is now {str_status.lower()}", ephemeral=True
            )
            return

        await interaction.response.send_message("You did not start the config process")

    @discord.ui.button(
        label="Enable",
        style=discord.ButtonStyle.green,
        emoji="<:greenTick:596576670815879169>",
        row=0,
    )
    async def enable(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ) -> None:
        await self.set_cached_status(interaction, self.original_response, True)  # type: ignore

    @discord.ui.button(
        label="Disable",
        style=discord.ButtonStyle.red,
        emoji="<:redTick:596576672149667840>",
        row=0,
    )
    async def disable(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ) -> None:
        await self.set_cached_status(interaction, self.original_response, False)  # type: ignore

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


class ConfigMenuView(KumikoView):
    def __init__(self, bot: KumikoCore, ctx: KContext, config_cog: Config) -> None:
        super().__init__(ctx)
        self.config_cog = config_cog
        self.pool = bot.pool
        self.redis_pool = bot.redis_pool
        self.add_item(ConfigMenu(bot, ctx, config_cog))

    @discord.ui.button(label="Save and Finish", style=discord.ButtonStyle.green, row=1)
    async def save(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ) -> None:
        value_map = {
            "local_economy": "Economy",
            "redirects": "Redirects",
            "logs": "Logs",
            "pins": "Pins",
        }
        query = """
        UPDATE guild
        SET logs = $2,
            local_economy = $3,
            redirects = $4,
            pins = $5
        WHERE id = $1;
        """
        if interaction.guild is None:
            return

        guild_id = interaction.guild.id
        cache = GuildCacheHandler(guild_id, self.redis_pool)
        cached_status = self.config_cog.reserved_configs.get(guild_id)

        if cached_status is None:
            return

        change_desc = "\n".join(
            [f"{value_map[k]}: {v}" for k, v in cached_status.items()]
        )
        desc = f"The following changes were made:\n{change_desc}"

        new_config = GuildConfig(**cached_status)
        status_values = [v for v in cached_status.values()]

        await self.pool.execute(query, guild_id, *status_values)
        await cache.replace_config(".config", new_config)
        if guild_id in self.config_cog.reserved_configs:
            self.config_cog.reserved_configs.pop(guild_id)

        await interaction.response.defer()
        await interaction.edit_original_response(content=desc, embed=None, view=None)
        self.stop()
