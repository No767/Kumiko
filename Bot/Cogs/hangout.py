import asyncio

import discord
from discord.ext import commands
from kumikocore import KumikoCore
from Libs.cog_utils.hangout import is_help_thread
from Libs.cog_utils.redirects import can_close_threads, mark_as_resolved
from Libs.ui.redirects import ConfirmResolvedView

NOELLE_HANGOUT_HELP_CHANNEL_ID = 1145900494284402750


class Hangout(commands.Cog):
    """Noelle's Hangout commands (exclusive for that guild lol)"""

    def __init__(self, bot: KumikoCore) -> None:
        self.bot = bot

    @property
    def display_emoji(self) -> discord.PartialEmoji:
        return discord.PartialEmoji.from_str("<:himikocircle:1147399110282969148>")

    @is_help_thread()
    @commands.cooldown(1, 20, commands.BucketType.channel)
    @commands.command(name="solved", aliases=["is_solved"])
    async def solved(self, ctx: commands.Context) -> None:
        """Marks a thread as completed"""

        channel = ctx.channel
        if not isinstance(channel, discord.Thread):
            raise RuntimeError("This only works in threads")

        if can_close_threads(ctx) and ctx.invoked_with in ["solved"]:
            # Permissions.add_reaction and Permissions.read_message_history is required
            await ctx.message.add_reaction(discord.PartialEmoji(name="\U00002705"))
            await mark_as_resolved(channel, ctx.author)
            return
        else:
            prompt_message = f"<@!{channel.owner_id}>, would you like to mark this thread as solved? If this thread is not marked as resolved, then it will not be resolved. This has been requested by {ctx.author.mention}."
            view = ConfirmResolvedView(thread=channel, author=ctx.author, timeout=300.0)
            await ctx.send(content=prompt_message, view=view)

    # Just use R. Danny's version of this.
    @commands.Cog.listener()
    async def on_thread_create(self, thread: discord.Thread) -> None:
        if thread.parent_id != NOELLE_HANGOUT_HELP_CHANNEL_ID:
            return

        if len(thread.name) <= 20:
            low_quality_title = (
                "This thread has been automatically closed due to a potentially low quality title. "
                "Your title should be descriptive of the problem you are having.\n\n"
                "Please remake your thread with a new and more descriptive title."
            )
            try:
                await thread.send(low_quality_title)
            except discord.Forbidden as e:
                # Race condition with Discord...
                if e.code == 40058:
                    await asyncio.sleep(2)
                    await thread.send(low_quality_title)

            await thread.edit(archived=True, locked=True, reason="Low quality title.")
            return

        message = thread.get_partial_message(thread.id)
        try:
            await message.pin()
        except discord.HTTPException:
            pass

    @solved.error
    async def on_solved_error(self, ctx: commands.Context, error: Exception):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(
                f"This command is on cooldown. Try again in {error.retry_after:.2f}s"
            )


async def setup(bot: KumikoCore) -> None:
    await bot.add_cog(Hangout(bot))
