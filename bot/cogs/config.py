from __future__ import annotations

from typing import TYPE_CHECKING, Dict, List, Optional, Union

import asyncpg
import discord
import msgspec
from async_lru import alru_cache
from discord import app_commands
from discord.ext import commands, menus
from libs.types.config import ReservedConfig, ReservedLGC
from libs.ui.config import ConfigMenuView
from libs.utils import Embed, GuildContext, KContext, is_manager
from libs.utils.pages import KumikoPages
from libs.utils.prefix import get_prefix
from typing_extensions import Annotated

if TYPE_CHECKING:
    from kumikocore import KumikoCore


class GuildConfig(msgspec.Struct):
    prefix: list[str]
    economy: bool = False
    redirects: bool = True
    voice_summary: bool = False


class GuildLogsConfig(msgspec.Struct):
    bot: KumikoCore
    guild_id: int
    category_id: int
    channel_id: int
    broadcast_url: str

    @property
    def category_channel(self) -> Optional[discord.CategoryChannel]:
        guild = self.bot.get_guild(self.guild_id)
        return guild and guild.get_channel(self.category_id)  # type: ignore

    @property
    def logging_channel(self) -> Optional[discord.TextChannel]:
        guild = self.bot.get_guild(self.guild_id)
        return guild and guild.get_channel(self.channel_id)  # type: ignore


class GuildLogsWebhookDispatcher:
    def __init__(self, bot: KumikoCore, guild_id: int):
        self.bot = bot
        self.guild_id = guild_id
        self.session = self.bot.session
        self.pool = self.bot.pool

    async def get_logging_webhook(self) -> Optional[discord.Webhook]:
        config = await self.get_logs_config()
        if config is None:
            return None
        return discord.Webhook.from_url(url=config.broadcast_url, session=self.session)

    @alru_cache()
    async def get_logs_config(self) -> Optional[GuildLogsConfig]:
        query = """
        SELECT category_id, channel_id, broadcast_url
        FROM guild_logs_config
        WHERE guild_id = $1;
        """
        rows = await self.pool.fetchrow(query, self.guild_id)
        if rows is None:
            self.get_logs_config.cache_invalidate()
            return None

        config = GuildLogsConfig(bot=self.bot, guild_id=self.guild_id, **dict(rows))
        return config


class PrefixConverter(commands.Converter):
    async def convert(self, ctx: commands.Context, argument: str):
        user_id = ctx.bot.user.id
        if argument.startswith((f"<@{user_id}>", f"<@!{user_id}>")):
            raise commands.BadArgument("That is a reserved prefix already in use.")
        if len(argument) > 100:
            raise commands.BadArgument("That prefix is too long.")
        return argument


class ConfigSelectMenu(discord.ui.Select["ConfigMenu"]):
    def __init__(self, cogs: List[commands.Cog], bot: KumikoCore):
        super().__init__(
            placeholder="Select a category...", min_values=1, max_values=1, row=0
        )
        self.cogs = cogs
        self.__fill_options()

    def __fill_options(self) -> None:
        self.add_option(
            label="Index",
            emoji="\N{WAVING HAND SIGN}",
            value="__index",
            description="The help page showing how to use the bot.",
        )
        for cog in self.cogs:
            description = cog.description.split("\n", 1)[0] or None
            emoji = getattr(cog, "display_emoji", None)
            self.add_option(
                label=cog.qualified_name,
                value=cog.qualified_name,
                description=description,
                emoji=emoji,
            )

    async def callback(self, interaction: discord.Interaction) -> None:
        assert self.view is not None
        value = self.values[0]
        if value == "__index":
            # await self.view.rebind(FrontPageSource(), interaction)
            ...
        else:
            ...


class ConfigMenu(KumikoPages):
    def __init__(self, source: menus.PageSource, ctx: KContext):
        super().__init__(source, ctx=ctx, compact=True)

    async def rebind(
        self, source: menus.PageSource, interaction: discord.Interaction
    ) -> None:
        self.source = source
        self.current_page = 0

        await self.source._prepare_once()
        page = await self.source.get_page(0)
        kwargs = await self.get_kwargs_from_page(page)
        self._update_labels(0)
        await interaction.response.edit_message(**kwargs, view=self)


class Config(commands.Cog):
    """Configure prefixes, modules, and much more"""

    def __init__(self, bot: KumikoCore) -> None:
        self.bot = bot
        self.session = self.bot.session
        self.pool = self.bot.pool
        self.reserved_configs: Dict[int, ReservedConfig] = {}
        self.reserved_lgc: Dict[int, ReservedLGC] = {}

    @property
    def display_emoji(self) -> discord.PartialEmoji:
        return discord.PartialEmoji(name="\U0001f6e0")

    @alru_cache(maxsize=1024)
    async def get_guild_config(
        self, guild_id: int, connection: Union[asyncpg.Pool, asyncpg.Connection]
    ) -> Optional[GuildConfig]:
        """Obtains the config of the guild.

        This does not obtain the configuration of the logs,
        but merely only the guild configuration itself. This
        corountine is cached heavily

        Args:
            guild_id (int): Guild ID to use for config
            connection (Union[asyncpg.Pool, asyncpg.Connection]): The connection to use. Will use an pool if needed as well

        Returns:
            Optional[GuildConfig]: Returns the existing cached config. `None` if not found.
        """
        query = """
        SELECT prefix, economy, redirects, voice_summary
        FROM guild_config
        WHERE id = $1;
        """
        rows = await connection.fetchrow(query, guild_id)
        if rows is None:
            self.get_guild_config.cache_invalidate(guild_id, connection)
            return None
        return GuildConfig(**dict(rows))

    @is_manager()
    @commands.hybrid_group(name="configure", aliases=["config"], fallback="modules")
    async def config(self, ctx: GuildContext) -> None:
        """Configure the settings for the modules on Kumiko"""
        assert ctx.guild is not None

        value_map = {
            "economy": "Economy",
            "redirects": "Redirects",
            "voice_summary": "VoiceSummary",
        }
        query = """
        SELECT economy, redirects, voice_summary
        FROM guild_config
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
        self.bot.logger.info(
            f"Current Values: {[(k, v) for k, v, in reserved_conf.items()]}"
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
        embed.set_author(name="Kumiko's Configuration Menu", icon_url=self.bot.user.display_avatar.url)  # type: ignore
        await ctx.send(embed=embed, view=view)

    @is_manager()
    @commands.guild_only()
    @config.group(name="logs", fallback="settings")
    async def logs(self, ctx: GuildContext) -> None:
        """Configure logging settings"""
        # assert ctx.guild is not None

        # query = """
        # SELECT mod, eco, redirects
        # FROM logging_config
        # WHERE guild_id = $1;
        # """
        # rows = await self.pool.fetchrow(query, ctx.guild.id)
        # if rows is None:
        #     await ctx.send("Apparently guild is not in db")
        #     return

        # lgc_conf = ReservedLGC(**dict(rows))
        # self.reserved_lgc.setdefault(ctx.guild.id, lgc_conf)
        # view = LGCView(self.bot, self, ctx)
        # embed = Embed()
        # embed.description = """
        # If you are the owner or a server mod, this is logging panel!
        # This menu is meant for enabling/disabling the different types of logging.
        # """
        # embed.add_field(
        #     name="How to use",
        #     value="Click on the select menu, and enable/disable the selected feature. Once finished, just click the 'Finish' button",
        #     inline=False,
        # )
        await ctx.send("yes")

    @commands.cooldown(10, 30, commands.BucketType.guild)
    @logs.command(name="setup")
    @app_commands.describe(name="The name of the channel. Defaults to kumiko-logs")
    async def logs_setup(self, ctx: GuildContext, *, name: Optional[str]) -> None:
        """First-time setup command for logging"""
        await ctx.defer()
        name = name or "kumiko-logs"
        guild_id = ctx.guild.id
        query = """
        INSERT INTO guild_logs_config (guild_id, category_id, channel_id, broadcast_url)
        VALUES ($1, $2, $3, $4);
        """

        webhook_dispatcher = GuildLogsWebhookDispatcher(self.bot, guild_id)
        config = await webhook_dispatcher.get_logs_config()

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
                read_messages=False,
                send_messages=False,
                create_public_threads=False,
            ),
            ctx.guild.me: discord.PermissionOverwrite(
                read_messages=True,
                send_messages=True,
                manage_webhooks=True,
                create_public_threads=True,
                manage_threads=True,
            ),
        }
        reason = (
            f"{ctx.author} (ID: {ctx.author.id}) has created the event logs channel"
        )
        delete_reason = "Failed to create logs category and/or channel"
        try:
            kumiko_category = await ctx.guild.create_category(
                name="kumiko", overwrites=overwrites, position=0
            )
            channel = await kumiko_category.create_text_channel(
                name=name, reason=reason, position=0
            )
            broadcast_webhook = await channel.create_webhook(
                name="Kumiko Logs", avatar=avatar_bytes
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
                query,
                guild_id,
                kumiko_category.id,
                broadcast_webhook.channel_id,
                broadcast_webhook.url,
            )
        except asyncpg.UniqueViolationError:
            await kumiko_category.delete(reason=delete_reason)
            await channel.delete(reason=delete_reason)
            await ctx.send("Failed to create the channel due to an internal error")
        else:
            webhook_dispatcher.get_logs_config.cache_invalidate()
            await ctx.send(
                f"Event Logs channel created successfully! Logs created at {channel.mention}"
            )

    @commands.cooldown(10, 30, commands.BucketType.guild)
    @logs.command(name="delete")
    async def logs_delete(self, ctx: GuildContext):
        """Deletes logging channels permanently"""
        await ctx.defer()
        query = """
        DELETE FROM guild_logs_config WHERE guild_id = $1;
        """
        msg = "Are you sure you want to delete the logging channels permanently?"
        dispatcher = GuildLogsWebhookDispatcher(self.bot, ctx.guild.id)
        logs_config = await dispatcher.get_logs_config()
        confirm = await ctx.prompt(msg)
        if confirm:
            if logs_config is None:
                msg = (
                    "Could not find guild logs config. Perhaps you didn't set this up?"
                )
                await ctx.send(msg)
                return

            author = ctx.author
            reason = f"{author.name} (ID: {author.name}) has requested to delete the logging channel"

            if (
                logs_config.category_channel is not None
                and logs_config.logging_channel is not None
            ):
                try:
                    await logs_config.category_channel.delete(reason=reason)
                    await logs_config.logging_channel.delete(reason=reason)
                except discord.Forbidden:
                    await ctx.send(
                        "\N{NO ENTRY SIGN} I do not have permissions to delete channels and/or webhooks."
                    )
                    return
                except discord.HTTPException:
                    await ctx.send("\N{NO ENTRY SIGN} Unknown error happened")
                    return

            await self.pool.execute(query, ctx.guild.id)
            dispatcher.get_logs_config.cache_invalidate()
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
            UPDATE guild_config
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
            UPDATE guild_config
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
        UPDATE guild_config
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
        INSERT INTO guild_config (id, prefix) VALUES ($1, $2)
        ON CONFLICT (id) DO NOTHING;
        """
        await self.pool.execute(insert_query, guild.id, [])

    @commands.Cog.listener()
    async def on_guild_remove(self, guild: discord.Guild) -> None:
        await self.pool.execute("DELETE FROM guild_config WHERE id = $1", guild.id)

    @commands.Cog.listener()
    async def on_guild_channel_delete(self, channel: discord.abc.GuildChannel) -> None:
        if not isinstance(channel, discord.TextChannel):
            return

        webhook_dispatcher = GuildLogsWebhookDispatcher(self.bot, channel.guild.id)
        webhook_config = await webhook_dispatcher.get_logs_config()

        if webhook_config is None:
            return

        if (
            webhook_config.logging_channel is None
            or webhook_config.channel_id != channel.id
        ):
            return

        # Delete the unused entries
        delete_query = "DELETE FROM guild_logs_config WHERE guild_id = $1;"
        await self.pool.execute(delete_query, channel.guild.id)
        webhook_dispatcher.get_logs_config.cache_invalidate()


async def setup(bot: KumikoCore) -> None:
    await bot.add_cog(Config(bot))
