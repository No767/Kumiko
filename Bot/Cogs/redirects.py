from typing import Optional

import discord
from discord import PartialEmoji, app_commands
from discord.ext import commands
from kumikocore import KumikoCore
from Libs.cache import KumikoCache
from Libs.cog_utils.redirects import (
    can_close_threads,
    create_redirected_thread,
    is_redirects_enabled,
    is_thread,
    mark_as_resolved,
)
from Libs.ui.redirects import ConfirmResolvedView
from Libs.utils import is_manager

CANNOT_REDIRECT_OWN_MESSAGE = "You can't redirect your own messages."
# Required Perms (from discord.Permission):
# send_message_in_threads, manage_threads, create_public_threads, manage_messages
class Redirects(commands.Cog):
    """Redirects a conversation into a separate thread

    This module is intended when you have multiple overlapping conversations in an channel.
    This module should be used within your general channel or others.
    """

    def __init__(self, bot: KumikoCore) -> None:
        self.bot = bot
        self.pool = self.bot.pool
        self.redis_pool = self.bot.redis_pool
        self.redirects_path = ".redirects"
        self.redirects_ctx_menu = app_commands.ContextMenu(
            name="Redirect Conversation",
            callback=self.redirects_callback,
        )
        self.bot.tree.add_command(self.redirects_ctx_menu)

    @property
    def display_emoji(self) -> PartialEmoji:
        return PartialEmoji(name="\U0001f500")

    @commands.Cog.listener()
    async def on_thread_create(self, thread: discord.Thread) -> None:
        # this logic is the same as RoboDanny
        # Requires Permissions.manage_messages
        message = thread.get_partial_message(thread.id)
        try:
            await message.pin()
        except discord.HTTPException:
            pass

    @property
    def configurable(self) -> bool:
        return True

    @is_redirects_enabled()
    @app_commands.checks.cooldown(1, 30, key=lambda i: (i.guild_id, i.user.id))
    async def redirects_callback(
        self, interaction: discord.Interaction, message: discord.Message
    ) -> None:
        """Redirects a conversation into a separate thread"""
        channel = interaction.channel

        if isinstance(channel, discord.TextChannel):
            if interaction.user.id == message.author.id:
                await interaction.response.send_message(
                    CANNOT_REDIRECT_OWN_MESSAGE, ephemeral=True
                )
                return

            reference_author = message.author
            author = interaction.user

            default_thread_name = f"{author.display_name} and {reference_author.display_name}'s conversation"
            redirected_thread = await create_redirected_thread(
                channel=channel,
                thread_name=default_thread_name,
                reason=f"Conversation redirected by {author.global_name}",
                msg=message,
                author=author,
                reference_author=reference_author,
            )
            await interaction.response.send_message(
                f"Notified {reference_author.display_name} to redirect the conversation to {redirected_thread}"
            )
            return

        await interaction.response.send_message(
            "This needs to be sent from a text channel", ephemeral=True
        )

    @is_redirects_enabled()
    @commands.cooldown(1, 30, commands.BucketType.user)
    @commands.command(name="redirect")
    async def redirect(
        self, ctx: commands.Context, *, thread_name: Optional[str] = None
    ) -> None:
        """Redirects a conversation into a separate thread"""
        msg = ctx.message.reference

        if msg is None:
            await ctx.send(
                "You need to reply to a user's message in order to use this."
            )
            return

        if isinstance(ctx.channel, discord.TextChannel):
            if msg and msg.cached_message is not None:
                reference_author = msg.cached_message.author

                if reference_author.id == ctx.author.id:
                    await ctx.send(CANNOT_REDIRECT_OWN_MESSAGE)
                    return

                default_thread_name = f"{ctx.author.display_name} and {reference_author.display_name}'s conversation"
                redirected_thread = await create_redirected_thread(
                    channel=ctx.channel,
                    thread_name=thread_name or default_thread_name,
                    reason=f"Conversation redirected by {ctx.author.name}",
                    msg=msg.cached_message,
                    author=ctx.author,
                    reference_author=reference_author,
                )
                await ctx.send(
                    f"Notified {reference_author.display_name} to redirect the conversation to {redirected_thread}"
                )
        else:
            await ctx.send(
                "You can't use this on other types of channels. Only text channels are able to redirect messages."
            )

    @commands.hybrid_group(name="redirects")
    async def redirects(self, ctx: commands.Context) -> None:
        """Module to handle redirecting replied conversations into threads"""
        if ctx.invoked_subcommand is None:
            await ctx.send_help(ctx.command)

    @is_manager()
    @redirects.command(name="enable")
    async def enable(self, ctx: commands.Context):
        """Enables the redirect module"""
        assert ctx.guild is not None
        key = f"cache:kumiko:{ctx.guild.id}:guild_config"
        cache = KumikoCache(self.redis_pool)
        query = """
        UPDATE guild
        SET redirects = $2
        WHERE id = $1;
        """
        results = await cache.get_json_cache(
            key=key, path=self.redirects_path, value_only=False
        )
        if results is True:
            await ctx.send("Redirects are already enabled")
            return
        else:
            await self.pool.execute(query, ctx.guild.id, True)
            await cache.merge_json_cache(
                key=key, value=True, path=self.redirects_path, ttl=None
            )
            await ctx.send("Redirects are now enabled")
            return

    @is_manager()
    @is_redirects_enabled()
    @redirects.command(name="disable")
    async def disable(self, ctx: commands.Context):
        """Disables the redirects module"""
        assert ctx.guild is not None
        key = f"cache:kumiko:{ctx.guild.id}:guild_config"
        cache = KumikoCache(connection_pool=self.redis_pool)
        query = """
        UPDATE guild
        SET redirects = $2
        WHERE id = $1;
        """
        await self.pool.execute(query, ctx.guild.id, False)
        await cache.merge_json_cache(
            key=key, value=False, path=self.redirects_path, ttl=None
        )
        await ctx.send(
            "Redirects is now disabled for your server. Please enable it first."
        )

    @is_thread()
    @is_redirects_enabled()
    @commands.cooldown(1, 20, commands.BucketType.channel)
    @commands.hybrid_command(name="resolved", aliases=["completed"])
    async def resolved(self, ctx: commands.Context) -> None:
        """Marks a thread as completed"""
        channel = ctx.channel
        if not isinstance(channel, discord.Thread):
            raise RuntimeError("This only works in threads")

        if can_close_threads(ctx) and ctx.invoked_with in [
            "resolved",
            "completed",
        ]:
            # Permissions.add_reaction and Permissions.read_message_history is required
            await ctx.message.add_reaction(discord.PartialEmoji(name="\U00002705"))
            await mark_as_resolved(channel, ctx.author)
            return
        else:
            prompt_message = f"<@!{channel.owner_id}>, would you like to mark this thread as solved? If this thread is not marked as resolved, then it will not be resolved. This has been requested by {ctx.author.mention}."
            view = ConfirmResolvedView(
                ctx=ctx, thread=channel, author=ctx.author, timeout=300.0
            )
            await ctx.send(content=prompt_message, view=view)

    @resolved.error
    async def on_resolved_error(self, ctx: commands.Context, error: Exception):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(
                f"This command is on cooldown. Try again in {error.retry_after:.2f}s"
            )


async def setup(bot: KumikoCore) -> None:
    await bot.add_cog(Redirects(bot))
