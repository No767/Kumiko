from typing import Union

import discord
from discord.ext import commands


def can_close_threads(ctx: commands.Context):
    if not isinstance(ctx.channel, discord.Thread):
        return False

    permissions = ctx.channel.permissions_for(ctx.author)  # type: ignore # discord.Member is a subclass of discord.User
    return permissions.manage_threads or ctx.channel.owner_id == ctx.author.id


async def mark_as_resolved(
    thread: discord.Thread, user: Union[discord.User, discord.Member]
) -> None:
    await thread.edit(
        locked=True,
        archived=True,
        reason=f"Marked as resolved by {user.global_name} (ID: {user.id})",
    )
