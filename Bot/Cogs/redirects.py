import discord
from discord import PartialEmoji, app_commands
from discord.ext import commands
from kumikocore import KumikoCore
from Libs.cache import KumikoCache
from Libs.cog_utils.redirects import (
    can_close_threads,
    is_redirects_enabled,
    is_thread,
    mark_as_resolved,
)
from Libs.ui.redirects import ConfirmResolvedView
from Libs.utils import is_manager


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

    @property
    def display_emoji(self) -> PartialEmoji:
        return PartialEmoji(name="\U0001f500")

    @commands.Cog.listener()
    async def on_thread_create(self, thread: discord.Thread) -> None:
        # this logic is the same as RoboDanny
        message = thread.get_partial_message(thread.id)
        try:
            await message.pin()
        except discord.HTTPException:
            pass

    @is_redirects_enabled()
    @commands.cooldown(1, 30, commands.BucketType.channel)
    @commands.hybrid_group(name="redirect", fallback="conversation")
    @app_commands.describe(thread_name="The name of the thread to create")
    async def redirect(self, ctx: commands.Context, *, thread_name: str) -> None:
        """Redirects a conversation into a separate thread"""
        # Requires Permissions.create_public_threads
        if (ctx.channel, discord.TextChannel):
            created_thread = await ctx.message.create_thread(
                name=thread_name, reason=f"Conversation redirected by {ctx.author.name}"
            )
            if ctx.message.reference is not None:
                reference_author = (
                    ctx.message.reference.cached_message.author.mention
                    if ctx.message.reference.cached_message is not None
                    else "you"
                )
                await ctx.send(
                    f"Hey, {ctx.author.mention} has requested that {reference_author} redirect this conversation to {created_thread.jump_url} instead."
                )
            else:
                await ctx.send(
                    f"{ctx.author.global_name} has requested that the conversation be moved to {created_thread.jump_url} instead."
                )
        else:
            await ctx.send(
                "You need to be in a text channel in order for this to work",
                ephemeral=True,
            )

    @is_manager()
    @redirect.command(name="enable")
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
            key=key, path="self.redirects_path", value_only=False
        )
        if results is True:
            await ctx.send("Redirects are already enabled")
            return
        else:
            await self.pool.execute(query, ctx.guild.id, True)
            await cache.merge_json_cache(
                key=key, value=True, path="self.redirects_path", ttl=None
            )
            await ctx.send("Redirects are now enabled")
            return

    @is_manager()
    @is_redirects_enabled()
    @redirect.command(name="disable")
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
            key=key, value=False, path="self.redirects_path", ttl=None
        )
        await ctx.send(
            "Redirects is now disabled for your server. Please enable it first."
        )

    @is_thread()
    @is_redirects_enabled()
    @commands.cooldown(1, 20, commands.BucketType.channel)
    @commands.hybrid_command(name="resolved", aliases=["completed", "solved"])
    async def resolved(self, ctx: commands.Context) -> None:
        """Marks a thread as completed"""
        channel = ctx.channel
        if not isinstance(channel, discord.Thread):
            raise RuntimeError("This only works in threads")

        if can_close_threads(ctx) and ctx.invoked_with in [
            "resolved",
            "completed",
            "solved",
        ]:
            # Permissions.add_reaction and Permissions.read_message_history is required
            await ctx.message.add_reaction(discord.PartialEmoji(name="\U00002705"))
            await mark_as_resolved(channel, ctx.author)
            return
        else:
            prompt_message = f"<@!{channel.owner_id}>, would you like to mark this thread as solved? If this thread is not marked as resolved, then it will not be resolved. This has been requested by {ctx.author.mention}."
            view = ConfirmResolvedView(thread=channel, author=ctx.author, timeout=300.0)
            await ctx.send(content=prompt_message, view=view)

    @resolved.error
    async def on_resolved_error(self, ctx: commands.Context, error: Exception):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(
                f"This command is on cooldown. Try again in {error.retry_after:.2f}s"
            )


async def setup(bot: KumikoCore) -> None:
    await bot.add_cog(Redirects(bot))
