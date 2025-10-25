from __future__ import annotations

import contextlib
from typing import TYPE_CHECKING, Optional, Union

import discord
from discord import app_commands
from discord.ext import commands

from utils.checks import bot_check_permissions
from utils.view import KumikoView

if TYPE_CHECKING:
    from discord.ext.commands._types import Check

    from core import Kumiko
    from utils.context import GuildContext

CANNOT_REDIRECT_OWN_MESSAGE = "You can't redirect your own messages."

### Command checks


def is_thread() -> Check[GuildContext]:
    def pred(ctx: commands.Context):
        return isinstance(ctx.channel, discord.Thread) and not isinstance(
            ctx.channel, discord.ForumChannel
        )

    return commands.check(pred)


### UI Components (Views)
class ConfirmResolvedView(KumikoView):
    def __init__(
        self,
        ctx: GuildContext,
        thread: discord.Thread,
        author: Union[discord.User, discord.Member],
        **kwargs,
    ) -> None:
        super().__init__(ctx, **kwargs)
        self.thread = thread
        self.author = author
        self.cog: Redirects = ctx.bot.get_cog("Redirects")  # type: ignore

    @discord.ui.button(
        label="Confirm",
        style=discord.ButtonStyle.green,
        emoji="<:greenTick:596576670815879169>",
    )
    async def confirm(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ) -> None:
        # Avoid relocking locked threads
        if self.thread.locked:
            return

        await interaction.response.send_message(
            "Marking this as solved. Next time you can mark it resolved yourself by using the command `>resolved`"
        )

        if interaction.message:
            await interaction.message.add_reaction(
                discord.PartialEmoji(name="\U00002705")
            )
            await self.cog.mark_as_resolved(self.thread, self.author)

    @discord.ui.button(
        label="Cancel",
        style=discord.ButtonStyle.red,
        emoji="<:redTick:596576672149667840>",
    )
    async def cancel(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ) -> None:
        await interaction.delete_original_response()
        self.stop()


# Required Perms (from discord.Permission):
# send_message_in_threads, manage_threads, create_public_threads, manage_messages
class Redirects(commands.Cog):
    """Redirects a conversation into a separate thread

    This module is intended when you have multiple overlapping conversations in an channel.
    This module should be used within your general channel or others.
    """

    def __init__(self, bot: Kumiko) -> None:
        self.bot = bot
        self.redirects_ctx_menu = app_commands.ContextMenu(
            name="Redirect Conversation",
            callback=self.redirects_callback,
        )
        self.bot.tree.add_command(self.redirects_ctx_menu)

    @property
    def display_emoji(self) -> discord.PartialEmoji:
        return discord.PartialEmoji(name="\U0001f500")

    ### Thread closure utilities

    def can_close_threads(self, ctx: GuildContext) -> bool:
        if not isinstance(ctx.channel, discord.Thread):
            return False

        permissions = ctx.channel.permissions_for(ctx.author)
        return permissions.manage_threads or ctx.channel.owner_id == ctx.author.id

    async def mark_as_resolved(
        self, thread: discord.Thread, user: Union[discord.User, discord.Member]
    ) -> None:
        await thread.edit(
            locked=True,
            archived=True,
            reason=f"Marked as resolved by {user.global_name} (ID: {user.id})",
        )

    async def create_redirected_thread(
        self,
        channel: discord.TextChannel,
        thread_name: str,
        reason: str,
        msg: discord.Message,
        author: Union[discord.User, discord.Member],
        reference_author: Union[discord.User, discord.Member],
    ) -> str:
        thread_name = (
            thread_name
            or f"{author.display_name} and {reference_author.display_name}'s conversation"
        )
        starter_message = (
            f"Hey, {author.mention} has requested that {reference_author.mention} redirect the conversation to this thread instead. "
            "You can mark this conversation as completed by using the command `>resolved` within this thread. "
            f"A reference message is provided from the earlier conversation here ({msg.jump_url}):\n\n"
            f"{msg.clean_content}"
        )
        created_thread = await channel.create_thread(
            name=thread_name, reason=reason, type=discord.ChannelType.public_thread
        )
        await created_thread.join()
        await created_thread.send(starter_message, suppress_embeds=True)
        return created_thread.jump_url

    ### Misc utilities

    async def _handle_cooldown_error(
        self, ctx: GuildContext, error: commands.CommandError
    ) -> None:
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(
                f"This command is on cooldown. Try again in {error.retry_after:.2f}s"
            )

    @app_commands.checks.cooldown(1, 30, key=lambda i: (i.guild_id, i.user.id))
    async def redirects_callback(
        self, interaction: discord.Interaction, message: discord.Message
    ) -> None:
        """Redirects a conversation into a separate thread"""
        if isinstance(interaction.channel, discord.TextChannel):
            if interaction.user.id == message.author.id:
                await interaction.response.send_message(
                    CANNOT_REDIRECT_OWN_MESSAGE, ephemeral=True
                )
                return

            reference_author = message.author
            author = interaction.user

            default_thread_name = f"{author.display_name} and {reference_author.display_name}'s conversation"
            redirected_thread = await self.create_redirected_thread(
                channel=interaction.channel,
                thread_name=default_thread_name,
                reason=f"Conversation redirected by {author.global_name}",
                msg=message,
                author=author,
                reference_author=reference_author,
            )
            self.bot.metrics.features.successful_redirects.inc()
            await interaction.response.send_message(
                f"Notified {reference_author.display_name} to redirect the conversation to {redirected_thread}"
            )
            return

        await interaction.response.send_message(
            "This needs to be sent from a text channel", ephemeral=True
        )

    @commands.cooldown(1, 30, commands.BucketType.user)
    @commands.command(name="redirect")
    async def redirect(self, ctx: GuildContext, *, thread_name: Optional[str]) -> None:
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
                redirected_thread = await self.create_redirected_thread(
                    channel=ctx.channel,
                    thread_name=thread_name or default_thread_name,
                    reason=f"Conversation redirected by {ctx.author.name}",
                    msg=msg.cached_message,
                    author=ctx.author,
                    reference_author=reference_author,
                )
                self.bot.metrics.features.successful_redirects.inc()
                await ctx.send(
                    f"Notified {reference_author.display_name} to redirect the conversation to {redirected_thread}"
                )
        else:
            await ctx.send(
                "You can't use this on other types of channels. Only text channels are able to redirect messages."
            )

    @is_thread()
    @bot_check_permissions(add_reactions=True, read_message_history=True)
    @commands.cooldown(1, 20, commands.BucketType.channel)
    @commands.command(name="resolved", aliases=["completed"])
    async def resolved(self, ctx: GuildContext) -> None:
        """Marks a thread as completed"""
        channel = ctx.channel
        if not isinstance(channel, discord.Thread):
            raise RuntimeError("This only works in threads")  # noqa: TRY004

        if self.can_close_threads(ctx) and ctx.invoked_with in [
            "resolved",
            "completed",
        ]:
            # Permissions.add_reaction and Permissions.read_message_history is required
            await ctx.message.add_reaction(discord.PartialEmoji(name="\U00002705"))
            await self.mark_as_resolved(channel, ctx.author)
        else:
            prompt_message = f"<@!{channel.owner_id}>, would you like to mark this thread as solved? If this thread is not marked as resolved, then it will not be resolved. This has been requested by {ctx.author.mention}."
            view = ConfirmResolvedView(
                ctx=ctx, thread=channel, author=ctx.author, timeout=300.0
            )
            await ctx.send(content=prompt_message, view=view)

    @commands.Cog.listener()
    async def on_thread_create(self, thread: discord.Thread) -> None:
        # this logic is the same as RoboDanny
        # Requires Permissions.manage_messages
        message = thread.get_partial_message(thread.id)
        with contextlib.suppress(discord.HTTPException):
            await message.pin()

    ### Error Handlers

    @redirect.error
    async def on_redirect_error(
        self, ctx: GuildContext, error: commands.CommandError
    ) -> None:
        await self._handle_cooldown_error(ctx, error)

    @resolved.error
    async def on_resolved_error(
        self, ctx: GuildContext, error: commands.CommandError
    ) -> None:
        await self._handle_cooldown_error(ctx, error)


async def setup(bot: Kumiko) -> None:
    await bot.add_cog(Redirects(bot))
