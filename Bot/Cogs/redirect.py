import discord
from discord import PartialEmoji, app_commands
from discord.ext import commands
from kumikocore import KumikoCore
from Libs.cog_utils.redirects import can_close_threads, is_thread, mark_as_resolved


class Redirect(commands.Cog):
    """Redirects a conversation into a separate thread"""

    def __init__(self, bot: KumikoCore) -> None:
        self.bot = bot

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

    @commands.has_permissions(create_public_threads=True)
    @commands.hybrid_command(name="redirect")
    @app_commands.describe(thread_name="The name of the thread to create")
    async def redirect(self, ctx: commands.Context, *, thread_name: str) -> None:
        """Redirects a conversation into a separate thread"""
        created_thread = await ctx.message.create_thread(
            name=thread_name, reason=f"Conversation redirected by {ctx.author.name}"
        )
        await created_thread.join()
        if ctx.message.reference is not None:
            reference_author = (
                ctx.message.reference.cached_message.author.mention
                if ctx.message.reference.cached_message is not None
                else "you"
            )
            await ctx.send(
                f"Hey, {ctx.author.mention} has requested that {reference_author} redirect this conversation to {created_thread.jump_url} instead."
            )
            return
        await ctx.send(
            f"Hey, {ctx.author.mention} redirected this conversation to {created_thread.jump_url} instead."
        )

    @is_thread()
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
            await ctx.message.add_reaction(
                discord.PartialEmoji.from_str("<:greenTick:596576670815879169>")
            )
            await mark_as_resolved(channel, ctx.author)
            return
        # await channel.edit(archived=True, locked=True)
        # await ctx.send("Marked as completed")


async def setup(bot: KumikoCore) -> None:
    await bot.add_cog(Redirect(bot))
