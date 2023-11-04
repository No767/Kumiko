from typing import Dict

import discord
from discord.ext import commands
from kumikocore import KumikoCore
from Libs.cog_utils.config import ReservedConfig, ReservedLGC
from Libs.ui.config import ConfigMenuView, LGCView
from Libs.utils import Embed, is_manager


class Config(commands.Cog):
    """Custom configuration layer for Kumiko"""

    def __init__(self, bot: KumikoCore) -> None:
        self.bot = bot
        self.pool = self.bot.pool
        self.redis_pool = self.bot.redis_pool
        self.reserved_configs: Dict[int, ReservedConfig] = {}
        self.reserved_lgc: Dict[int, ReservedLGC] = {}

    def is_lgc_already_enabled(self, guild_id: int, type: str):
        conf = self.reserved_lgc.get(guild_id)
        if conf is None:
            return

        return conf[type]

    def is_config_already_enabled(self, guild_id: int, type: str):
        value_to_key = {
            "Economy": "local_economy",
            "Redirects": "redirects",
            "EventsLog": "logs",
            "Pins": "pins",
        }
        conf = self.reserved_configs.get(guild_id)
        if conf is None:
            return
        key = value_to_key[type]
        return conf[key]

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
        self.reserved_configs.setdefault(ctx.guild.id, reserved_conf)
        view = ConfigMenuView(self.bot, ctx, self)
        embed = Embed()
        embed.description = """
        If you are the owner or a server mod, this is the main configuration menu!
        This menu is meant for enabling/disabling features.
        """
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
        self.reserved_lgc.setdefault(ctx.guild.id, lgc_conf)
        view = LGCView(self.bot, self, ctx)
        embed = Embed()
        embed.description = """
        If you are the owner or a server mod, this is logging panel!
        This menu is meant for enabling/disabling the different types of logging.
        """
        embed.add_field(
            name="How to use",
            value="Click on the select menu, and enable/disable the selected feature. Once finished, just click the 'Finish' button",
            inline=False,
        )
        await ctx.send(embed=embed, view=view)


async def setup(bot: KumikoCore) -> None:
    await bot.add_cog(Config(bot))
