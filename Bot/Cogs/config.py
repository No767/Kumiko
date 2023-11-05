from typing import Dict

import discord
from discord import app_commands
from discord.ext import commands
from kumikocore import KumikoCore
from Libs.cog_utils.config import PrefixConverter, ReservedConfig, ReservedLGC
from Libs.errors import ValidationError
from Libs.ui.config import ConfigMenuView, DeletePrefixView, LGCView
from Libs.utils import ConfirmEmbed, Embed, get_prefix, is_manager


class Config(commands.Cog):
    """Configure prefixes, modules, and much more"""

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
    @commands.hybrid_group(name="configure", aliases=["config"], fallback="modules")
    async def config(self, ctx: commands.Context) -> None:
        """Configure the settings for the modules on Kumiko"""
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

    @commands.guild_only()
    @config.group(name="prefix", fallback="info")
    async def prefix(self, ctx: commands.Context) -> None:
        """Displays info about the current prefix set on your server"""
        prefixes = await get_prefix(self.bot, ctx.message)
        cleaned_prefixes = ", ".join([f"`{item}`" for item in prefixes]).rstrip(",")
        embed = Embed()
        embed.description = f"**Current prefixes**\n{cleaned_prefixes}"
        embed.timestamp = discord.utils.utcnow()
        embed.set_author(name=ctx.guild.name, icon_url=ctx.guild.icon.url)  # type: ignore # LIES, LIES, AND LIES!!!
        await ctx.send(embed=embed)

    @is_manager()
    @commands.guild_only()
    @prefix.command(name="update")
    @app_commands.describe(
        old_prefix="The old prefix to replace", new_prefix="The new prefix to use"
    )
    async def update(
        self, ctx: commands.Context, old_prefix: str, new_prefix: PrefixConverter
    ) -> None:
        """Updates the prefix for your server"""
        query = """
            UPDATE guild
            SET prefix = ARRAY_REPLACE(prefix, $1, $2)
            WHERE id = $3;
        """
        guild_id = ctx.guild.id  # type: ignore
        if old_prefix in self.bot.prefixes[guild_id]:
            await self.pool.execute(query, old_prefix, new_prefix, guild_id)
            prefixes = self.bot.prefixes[guild_id][
                :
            ]  # Shallow copy the list so we can safely perform operations on it
            for idx, item in enumerate(prefixes):
                if item == old_prefix:
                    prefixes[idx] = new_prefix
            self.bot.prefixes[guild_id] = prefixes
            await ctx.send(f"Prefix updated to `{new_prefix}`")
        else:
            await ctx.send("The prefix is not in the list of prefixes for your server")

    @is_manager()
    @commands.guild_only()
    @prefix.command(name="add")
    @app_commands.describe(prefix="The new prefix to add")
    async def add(self, ctx: commands.Context, prefix: PrefixConverter) -> None:
        """Adds new prefixes into your server"""
        prefixes = await get_prefix(self.bot, ctx.message)
        # validatePrefix(self.bot.prefixes, prefix) is False
        if len(prefixes) > 10:
            desc = "There was an validation issue. This is because of two reasons:\n- You have more than 10 prefixes for your server\n- Your prefix fails the validation rules"
            raise ValidationError(desc)

        if prefix in self.bot.prefixes[ctx.guild.id]:  # type: ignore
            await ctx.send("The prefix you want to set already exists")
            return

        query = """
            UPDATE guild
            SET prefix = ARRAY_APPEND(prefix, $1)
            WHERE id=$2;
        """
        guild_id = ctx.guild.id  # type: ignore # These are all done in an guild
        await self.pool.execute(query, prefix, guild_id)
        # the weird solution but it actually works
        if isinstance(self.bot.prefixes[guild_id], list):
            self.bot.prefixes[guild_id].append(prefix)
        else:
            self.bot.prefixes[guild_id] = [self.bot.default_prefix, prefix]
        await ctx.send(f"Added prefix: {prefix}")

    @is_manager()
    @commands.guild_only()
    @prefix.command(name="delete")
    @app_commands.describe(prefix="The prefix to delete")
    async def delete(self, ctx: commands.Context, prefix: str) -> None:
        """Deletes a prefix from your server"""
        view = DeletePrefixView(bot=self.bot, ctx=ctx, prefix=prefix)
        embed = ConfirmEmbed()
        embed.description = f"Do you want to delete the following prefix: {prefix}"
        await ctx.send(embed=embed, view=view)


async def setup(bot: KumikoCore) -> None:
    await bot.add_cog(Config(bot))
