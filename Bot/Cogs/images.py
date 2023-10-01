from functools import partial
from typing import Optional

import discord
from discord import PartialEmoji, app_commands
from discord.ext import commands
from kumikocore import KumikoCore
from Libs.cog_utils.images import (
    obtain_avatar_bytes,
    process_circle_image,
    process_image,
)


class Images(commands.Cog):
    """Image cmds"""

    def __init__(self, bot: KumikoCore) -> None:
        self.bot = bot

    @property
    def display_emoji(self) -> PartialEmoji:
        return PartialEmoji(name="\U0001f58c")

    @commands.hybrid_command(name="avatar-border")
    @app_commands.describe(user="The user to draw")
    async def avatar_border(
        self, ctx: commands.Context, user: Optional[discord.Member] = None
    ) -> None:
        """Draw a border"""
        await ctx.defer()
        member = user or ctx.author
        member_colour = (0, 0, 0)

        if isinstance(member, discord.Member):
            # get the user's colour, pretty self explanatory
            member_colour = member.colour.to_rgb()

        # grab the user's avatar as bytes
        avatar_bytes = await obtain_avatar_bytes(member)

        # create partial function so we don't have to stack the args in run_in_executor
        fn = partial(process_image, avatar_bytes, member_colour)  # type: ignore

        # this runs our processing in an executor, stopping it from blocking the thread loop.
        # as we already seeked back the buffer in the other thread, we're good to go
        final_buffer = await self.bot.loop.run_in_executor(None, fn)

        # prepare the file
        file = discord.File(filename="circle.png", fp=final_buffer)

        # send it
        await ctx.send(file=file)

    @commands.hybrid_command(name="circle-avatar")
    @app_commands.describe(user="The user to draw")
    async def avatar_border(
        self, ctx: commands.Context, user: Optional[discord.Member] = None
    ) -> None:
        """Draw a circle"""
        await ctx.defer()
        member = user or ctx.author
        image_bytes = await obtain_avatar_bytes(member)

        final_buffer = await self.bot.loop.run_in_executor(
            None, process_circle_image, image_bytes
        )

        file = discord.File(filename="circle_image.png", fp=final_buffer)

        await ctx.send(file=file)


async def setup(bot: KumikoCore) -> None:
    await bot.add_cog(Images(bot))
