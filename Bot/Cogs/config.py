from typing import Dict, TypedDict

import discord
from discord.ext import commands
from kumikocore import KumikoCore
from Libs.cog_utils.config import ReservedConfig
from Libs.ui.config import ConfigMenuView, LGCView
from Libs.utils import Embed, is_manager


class ReservedLGC(TypedDict):
    mod: bool
    eco: bool
    redirects: bool


class Config(commands.Cog):
    """Custom configuration layer for Kumiko"""

    def __init__(self, bot: KumikoCore) -> None:
        self.bot = bot
        self.pool = self.bot.pool
        self.redis_pool = self.bot.redis_pool
        self._reserved_configs: Dict[int, ReservedConfig] = {}
        self._reserved_lgc: Dict[int, ReservedLGC] = {}

        self.events_name_list = ["member_events", "mod_events", "eco_events"]

    def add_lgc(self, guild_id: int, config: ReservedLGC):
        self._reserved_lgc.setdefault(guild_id, config)

    def is_lgc_in(self, guild_id: int) -> bool:
        return guild_id in self._reserved_lgc

    def get_cached_lgc(self, guild_id: int):
        return self._reserved_lgc.get(guild_id)

    def remove_lgc(self, guild_id: int) -> None:
        try:
            if guild_id in self._reserved_lgc:
                self._reserved_lgc.pop(guild_id)
        except KeyError:
            return

    def set_lgc(self, guild_id: int, type: str, status: bool) -> None:
        try:
            self._reserved_lgc[guild_id][type] = status
        except KeyError:
            return

    def add_in_progress_config(self, guild_id: int, config: ReservedConfig) -> None:
        self._reserved_configs.setdefault(guild_id, config)

    def is_config_in_progress(self, guild_id: int) -> bool:
        return guild_id in self._reserved_configs

    def check_lgc_value_enabled(self, guild_id: int, type: str):
        conf = self._reserved_lgc.get(guild_id)
        if conf is None:
            return

        return conf[type]

    def remove_in_progress_config(self, guild_id: int) -> None:
        try:
            if guild_id in self._reserved_configs:
                self._reserved_configs.pop(guild_id)
        except KeyError:
            return

    def set_status_in_progress(self, guild_id: int, type: str, status: bool):
        try:
            self._reserved_configs[guild_id][type] = status
        except KeyError:
            return

    def check_already_enabled(self, guild_id: int, type: str):
        value_to_key = {
            "Economy": "local_economy",
            "Redirects": "redirects",
            "EventsLog": "logs",
            "Pins": "pins",
        }
        conf = self._reserved_configs.get(guild_id)
        if conf is None:
            return
        key = value_to_key[type]
        return conf[key]

    def get_status_config(self, guild_id: int):
        return self._reserved_configs.get(guild_id)

    @property
    def display_emoji(self) -> discord.PartialEmoji:
        return discord.PartialEmoji(name="\U0001f6e0")

    @is_manager()
    @commands.hybrid_group(name="configure", aliases=["config"], fallback="features")
    async def config(self, ctx: commands.Context) -> None:
        """Configure the settings for Kumiko"""
        assert ctx.guild is not None

        query = """
        SELECT logs, local_economy, redirects, pins
        FROM guild
        WHERE id = $1;
        """
        rows = await self.pool.fetchrow(query, ctx.guild.id)
        if rows is None:
            await ctx.send("Is the guild in the DB?")
            return
        reserved_conf = ReservedConfig(**dict(rows))
        self.add_in_progress_config(ctx.guild.id, reserved_conf)
        before_setting_str = "\n".join([f"{k}: {v}" for k, v in reserved_conf.items()])
        view = ConfigMenuView(self.bot, ctx, self)
        embed = Embed()
        embed.description = """
        If you are the owner or a server mod, this is the main configuration menu!
        This menu is meant for enabling/disabling features.
        """
        embed.add_field(
            name="Before Setting Values (static; these do not update)",
            value=before_setting_str,
            inline=False,
        )
        embed.add_field(
            name="How to use",
            value="Click on the select menu, and enable/disable the selected feature. Once finished, just click the 'Finish' button",
            inline=False,
        )
        embed.set_author(name="Kumiko's Configuration Menu", icon_url=self.bot.user.display_avatar.url)  # type: ignore
        await ctx.send(embed=embed, view=view)

    @is_manager()
    @config.command(name="logs")
    async def logs(self, ctx: commands.Context) -> None:
        """Set up logging"""
        assert ctx.guild is not None

        query = """
        SELECT mod, eco, redirects
        FROM logging_config
        WHERE guild_id = $1;
        """
        rows = await self.pool.fetchrow(query, ctx.guild.id)
        if rows is None:
            await ctx.send("Apparently guild is not in db")
            return

        lgc_conf = ReservedLGC(**dict(rows))
        self.add_lgc(ctx.guild.id, lgc_conf)
        view = LGCView(self.bot, self, ctx)
        embed = Embed()
        desc = """
        This is the main panel to enable/disable logging features.
        """
        embed.description = desc
        await ctx.send(embed=embed, view=view)


async def setup(bot: KumikoCore) -> None:
    await bot.add_cog(Config(bot))
