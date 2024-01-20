from __future__ import annotations

from typing import TYPE_CHECKING, Optional, TypedDict

import discord
from Libs.utils import Embed, KContext, KumikoView

from .utils import determine_status, format_conf_desc

if TYPE_CHECKING:
    from Bot.Cogs.config import Config
    from Bot.kumikocore import KumikoCore


class ReservedConfig(TypedDict):
    economy: bool
    redirects: bool
    voice_summary: bool


class NewConfigMenu(discord.ui.Select):
    def __init__(self, bot: KumikoCore, ctx: KContext, config_cog: Config) -> None:
        self.bot = bot
        self.ctx = ctx
        self.config_cog = config_cog
        self.value_to_key = {
            "Economy": "economy",
            "Redirects": "redirects",
            "VoiceSummary": "voice_summary",
        }
        options = [
            discord.SelectOption(
                emoji=getattr(cog, "display_emoji", None),
                label=cog_name,
                description=cog.__doc__.split("\n")[0]
                if cog.__doc__ is not None
                else None,
                value=self.value_to_key[cog_name],
            )
            for cog_name, cog in self.bot.cogs.items()
            if getattr(cog, "configurable", None) is not None
        ]
        super().__init__(
            placeholder="Select a category...",
            min_values=1,
            max_values=3,
            options=options,
            row=0,
        )
        self.prev_selected: Optional[set] = None

    def tick(self, status) -> str:
        if status is True:
            return "\U00002705"
        return "\U0000274c"

    async def callback(self, interaction: discord.Interaction) -> None:
        if interaction.guild is None:
            raise RuntimeError("Wrong...")

        values = self.values
        current_selection = self.config_cog.reserved_configs.get(interaction.guild.id)
        if current_selection is None:
            await interaction.response.send_message(
                "No selection cached?", ephemeral=True
            )
            return

        output_selection = ReservedConfig(
            economy=False, redirects=False, voice_summary=False
        )
        if interaction.guild.id in self.config_cog.reserved_configs:
            output_selection = current_selection

        current_selected = set(self.values)

        if self.prev_selected is not None:
            missing = self.prev_selected - current_selected
            added = current_selected - self.prev_selected

            combined = missing.union(added)

            for tag in combined:
                output_selection[tag] = not current_selection[tag]
        else:
            for tag in values:
                output_selection[tag] = not current_selection[tag]

        self.config_cog.reserved_configs[interaction.guild.id] = output_selection
        self.prev_selected = set(self.values)
        formatted_str = "\n".join(
            f"{self.tick(v)} - {k.title()}" for k, v in output_selection.items()
        )
        result = f"The following have been modified:\n\n{formatted_str}"

        embed = Embed(title="Modified Tags")
        embed.description = result
        embed.set_footer(text="\U00002705 = Selected | \U0000274c = Unselected")
        await interaction.response.send_message(embed=embed, ephemeral=True)


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
            "Economy": "economy",
            "Redirects": "redirects",
            "VoiceSummary": "voice_summary",
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
            "Economy": "economy",
            "Redirects": "redirects",
            "VoiceSummary": "voice_summary",
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
        self.add_item(NewConfigMenu(bot, ctx, config_cog))

    async def on_timeout(self) -> None:
        if self.message and not self.triggered.is_set():
            await self.message.edit(embed=self.build_timeout_embed(), view=None)

    @discord.ui.button(label="Save and Finish", style=discord.ButtonStyle.green, row=1)
    async def save(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ) -> None:
        value_map = {
            "economy": "Economy",
            "redirects": "Redirects",
            "voice_summary": "VoiceSummary",
        }
        query = """
        UPDATE guild_config
        SET economy = $2,
            redirects = $3,
            voice_summary = $4
        WHERE id = $1;
        """
        if interaction.guild is None:
            return

        guild_id = interaction.guild.id
        cached_status = self.config_cog.reserved_configs.get(guild_id)

        if cached_status is None:
            return

        change_desc = "\n".join(
            [f"{value_map[k]}: {v}" for k, v in cached_status.items()]
        )
        desc = f"The following changes were made:\n{change_desc}"

        status_values = [v for v in cached_status.values()]

        await self.pool.execute(query, guild_id, *status_values)
        if guild_id in self.config_cog.reserved_configs:
            self.config_cog.reserved_configs.pop(guild_id)

        if self.message:
            self.triggered.set()
            await self.message.edit(content=desc, embed=None, view=None)
            self.stop()
