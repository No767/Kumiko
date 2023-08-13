from discord import PartialEmoji, app_commands
from discord.ext import commands
from kumikocore import KumikoCore
from Libs.cog_utils.redirects import is_thread


class Redirect(commands.Cog):
    """Redirects a conversation into a separate thread"""

    def __init__(self, bot: KumikoCore) -> None:
        self.bot = bot

    @property
    def display_emoji(self) -> PartialEmoji:
        return PartialEmoji(name="\U0001f500")

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
    @commands.hybrid_command(name="completed")
    async def completed(self, ctx: commands.Context) -> None:
        """Marks a thread as completed"""
        channel = ctx.channel
        await channel.edit(archived=True, locked=True)  # type: ignore
        await ctx.send("Marked as completed")


async def setup(bot: KumikoCore) -> None:
    await bot.add_cog(Redirect(bot))
