from typing import Dict, Optional, TypedDict

import asyncpg
import discord
from discord import app_commands
from discord.ext import commands
from libs.ui.config import ConfigMenuView, LGCView
from libs.utils import WebhookDispatcher, is_manager
from libs.utils.context import GuildContext
from libs.utils.embeds import Embed
from libs.utils.prefix import get_prefix
from typing_extensions import Annotated

from bot.kumiko import Kumiko


class ReservedConfig(TypedDict):
    logs: bool
    local_economy: bool
    redirects: bool
    pins: bool


class ReservedLGC(TypedDict):
    mod: bool
    eco: bool
    redirects: bool


class PrefixConverter(commands.Converter):
    async def convert(self, ctx: commands.Context, argument: str):
        user_id = ctx.bot.user.id
        if argument.startswith((f"<@{user_id}>", f"<@!{user_id}>")):
            raise commands.BadArgument("That is a reserved prefix already in use.")
        if len(argument) > 100:
            raise commands.BadArgument("That prefix is too long.")
        return argument


class Config(commands.Cog):
    """Configure prefixes, modules, and much more"""

    def __init__(self, bot: Kumiko) -> None:
        self.bot = bot
        self.session = self.bot.session
        self.pool = self.bot.pool
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
    async def config(self, ctx: GuildContext) -> None:
        """Configure the settings for the modules on Kumiko"""
        assert ctx.guild is not None

        value_map = {
            "local_economy": "Economy",
            "redirects": "Redirects",
            "logs": "Logs",
            "pins": "Pins",
        }
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
        current_status = "\n".join(
            [f"{value_map[k]}: {v}" for k, v in reserved_conf.items()]
        )
        view = ConfigMenuView(self.bot, ctx, self)
        embed = Embed()
        embed.description = """
        If you are the owner or a server mod, this is the main configuration menu!
        This menu is meant for enabling/disabling features.
        """
        embed.add_field(
            name="Last Saved Values", value=f"```{current_status}```", inline=False
        )
        embed.add_field(
            name="How to use",
            value="Click on the select menu, and enable/disable the selected feature. Once finished, just click the 'Finish' button",
            inline=False,
        )
        embed.set_author(
            name="Kumiko's Configuration Menu",
            icon_url=self.bot.user.display_avatar.url,
        )  # type: ignore
        await ctx.send(embed=embed, view=view)

    @is_manager()
    @commands.guild_only()
    @config.group(name="logs", fallback="settings")
    async def logs(self, ctx: GuildContext) -> None:
        """Configure logging settings"""
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

    @commands.cooldown(10, 30, commands.BucketType.guild)
    @logs.command(name="setup")
    @app_commands.describe(
        name="The name of the channel. Defaults to kumiko-events-log"
    )
    async def logs_setup(self, ctx: GuildContext, *, name: Optional[str]) -> None:
        """First-time setup command for logging"""
        assert ctx.guild is not None

        name = name or "kumiko-events-log"
        guild_id = ctx.guild.id
        query = """
        INSERT INTO logging_webhooks (id, channel_id, broadcast_url)
        VALUES ($1, $2, $3);
        """

        webhook_dispatcher = WebhookDispatcher(self.bot, guild_id)
        config = await webhook_dispatcher.get_webhook_config()
        if config is not None and config.logging_channel is not None:
            msg = (
                f"It seems like there is a channel set up at {config.logging_channel.mention}\n"
                f"If you want to delete it, please run the command `{ctx.prefix}config logs delete`"
            )
            await ctx.send(msg)
            return

        perms = ctx.channel.permissions_for(ctx.guild.me)

        if not perms.manage_webhooks or not perms.manage_channels:
            await ctx.send(
                "\N{NO ENTRY SIGN} I do not have proper permissions (Manage Webhooks and Manage Channel)"
            )
            return

        avatar_bytes = await self.bot.user.display_avatar.read()  # type: ignore # The bot should be logged in order to run this command
        overwrites = {
            ctx.guild.default_role: discord.PermissionOverwrite(
                read_messages=False, send_messages=False
            ),
            ctx.guild.me: discord.PermissionOverwrite(
                read_messages=True, send_messages=True, manage_webhooks=True
            ),
        }
        reason = (
            f"{ctx.author} (ID: {ctx.author.id}) has created the event logs channel"
        )

        try:
            channel = await ctx.guild.create_text_channel(
                name=name, overwrites=overwrites, reason=reason
            )
            broadcast_webhook = await channel.create_webhook(
                name="Kumiko Event Logs", avatar=avatar_bytes
            )
        except discord.Forbidden:
            await ctx.send(
                "\N{NO ENTRY SIGN} I do not have permissions to create a channel and/or webhooks."
            )
            return
        except discord.HTTPException:
            await ctx.send(
                "\N{NO ENTRY SIGN} This channel name is bad or an unknown error happened."
            )
            return

        try:
            await self.pool.execute(
                query, guild_id, broadcast_webhook.channel_id, broadcast_webhook.url
            )
            webhook_dispatcher.get_webhook_config.cache_invalidate(guild_id=guild_id)
            await ctx.send(f"EventLogs Channel created at {channel.mention}")
        except asyncpg.UniqueViolationError:
            await channel.delete(reason="Failed to create logs")
            await ctx.send("Failed to create the channel due to an internal error")

    @commands.cooldown(10, 30, commands.BucketType.guild)
    @logs.command(name="delete")
    async def logs_delete(self, ctx: GuildContext):
        """Deletes logging channels permanently"""
        query = """
        WITH delete_webhooks AS (
            DELETE FROM logging_webhooks
            WHERE id = $1
            RETURNING id
        )
        DELETE FROM logging_config
        WHERE guild_id = (SELECT id FROM delete_webhooks);
        """
        msg = "Are you sure you want to delete the logging channels permanently?"
        dispatcher = WebhookDispatcher(self.bot, ctx.guild.id)
        confirm = await ctx.prompt(msg)
        if confirm:
            webhook_config = await dispatcher.get_webhook_config()
            if webhook_config is None or webhook_config.logging_channel is None:
                msg = (
                    "Apparently you don't have a channel to begin with... "
                    f"Please run `{ctx.prefix}config logs setup` to make one"
                )
                await ctx.send(msg)
                return

            author = ctx.author
            reason = f"{author.name} (ID: {author.name}) has requested to delete the logging channel"

            try:
                await webhook_config.logging_channel.delete(reason=reason)
            except discord.Forbidden:
                await ctx.send(
                    "\N{NO ENTRY SIGN} I do not have permissions to delete channels and/or webhooks."
                )
                return
            except discord.HTTPException:
                await ctx.send("\N{NO ENTRY SIGN} Unknown error happened")
                return

            dispatcher.get_webhook_config.cache_invalidate()
            await self.pool.execute(query, ctx.guild.id)

            await ctx.send("Logging channels have been successfully deleted")
        elif confirm is None:
            await ctx.send("Not removing logging channels. Cancelling")
        else:
            await ctx.send("Cancelling")

    @commands.guild_only()
    @config.group(name="prefix", fallback="info")
    async def prefix(self, ctx: GuildContext) -> None:
        """Displays info about the current prefix set on your server"""
        prefixes = await get_prefix(self.bot, ctx.message)
        cleaned_prefixes = ", ".join([f"`{item}`" for item in prefixes]).rstrip(",")
        embed = Embed()
        embed.description = f"**Current prefixes**\n{cleaned_prefixes}"
        embed.timestamp = discord.utils.utcnow()
        embed.set_author(name=ctx.guild.name, icon_url=ctx.guild.icon.url)  # type: ignore # LIES, LIES, AND LIES!!!
        await ctx.send(embed=embed)

    @is_manager()
    @prefix.command(name="update")
    @app_commands.describe(old="The old prefix to replace", new="The new prefix to use")
    @app_commands.rename(old="old_prefix", new="new_prefix")
    async def update(
        self,
        ctx: GuildContext,
        old: Annotated[str, PrefixConverter],
        new: Annotated[str, PrefixConverter],
    ) -> None:
        """Updates the prefix for your server"""
        query = """
            UPDATE guild
            SET prefix = ARRAY_REPLACE(prefix, $1, $2)
            WHERE id = $3;
        """
        prefixes = await get_prefix(self.bot, ctx.message)

        guild_id = ctx.guild.id
        if old in prefixes:
            await self.pool.execute(query, old, new, guild_id)
            get_prefix.cache_invalidate(self.bot, ctx.message)
            await ctx.send(f"Prefix updated to `{new}`")
        else:
            await ctx.send("The prefix is not in the list of prefixes for your server")

    @is_manager()
    @prefix.command(name="add")
    @app_commands.describe(prefix="The new prefix to add")
    async def add(
        self, ctx: GuildContext, prefix: Annotated[str, PrefixConverter]
    ) -> None:
        """Adds new prefixes into your server"""
        prefixes = await get_prefix(self.bot, ctx.message)
        if isinstance(prefixes, list) and len(prefixes) > 10:
            desc = (
                "There was a validation issue. "
                "This is caused by these reasons: \n"
                "- You have more than 10 prefixes for your server\n"
                "- Your prefix fails the validation rules"
            )
            await ctx.send(desc)
            return

        if prefix in prefixes:
            await ctx.send("The prefix you want to set already exists")
            return

        query = """
            UPDATE guild
            SET prefix = ARRAY_APPEND(prefix, $1)
            WHERE id=$2;
        """
        await self.pool.execute(query, prefix, ctx.guild.id)
        get_prefix.cache_invalidate(self.bot, ctx.message)
        await ctx.send(f"Added prefix: {prefix}")

    @is_manager()
    @prefix.command(name="delete")
    @app_commands.describe(prefix="The prefix to delete")
    async def delete(
        self, ctx: GuildContext, prefix: Annotated[str, PrefixConverter]
    ) -> None:
        """Deletes a prefix from your server"""
        query = """
        UPDATE guild
        SET prefix = ARRAY_REMOVE(prefix, $1)
        WHERE id=$2;
        """
        msg = f"Do you want to delete the following prefix: {prefix}"
        confirm = await ctx.prompt(msg, timeout=120.0)
        if confirm:
            await self.pool.execute(query, prefix, ctx.guild.id)
            get_prefix.cache_invalidate(self.bot, ctx.message)
            await ctx.send(f"The prefix `{prefix}` has been successfully deleted")
            return
        await ctx.send("Confirmation cancelled. Please try again")

    @commands.Cog.listener()
    async def on_guild_join(self, guild: discord.Guild) -> None:
        insert_query = """
        INSERT INTO guild (id, prefix) VALUES ($1, $2)
        ON CONFLICT (id) DO NOTHING;
        """
        await self.pool.execute(insert_query, guild.id, [])

    @commands.Cog.listener()
    async def on_guild_remove(self, guild: discord.Guild) -> None:
        await self.pool.execute("DELETE FROM guild WHERE id = $1", guild.id)

    @commands.Cog.listener()
    async def on_guild_channel_delete(self, channel: discord.abc.GuildChannel) -> None:
        if not isinstance(channel, discord.TextChannel):
            return

        webhook_dispatcher = WebhookDispatcher(self.bot, channel.guild.id)
        webhook_config = await webhook_dispatcher.get_webhook_config()

        if webhook_config is None:
            return

        if (
            webhook_config.logging_channel is None
            or webhook_config.channel_id != channel.id
        ):
            return

        # Delete the unused entries
        delete_query = "DELETE FROM logging_webhooks WHERE id = $1;"
        await self.pool.execute(delete_query, channel.guild.id)
        webhook_dispatcher.get_webhook_config.cache_invalidate()


async def setup(bot: Kumiko) -> None:
    await bot.add_cog(Config(bot))
