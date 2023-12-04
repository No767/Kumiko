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


async def create_redirected_thread(
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
