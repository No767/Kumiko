from typing import Optional

import discord


async def get_or_fetch_member(
    guild: discord.Guild, member_id: int
) -> Optional[discord.Member]:
    member = guild.get_member(member_id)
    if member is not None:
        return member
    members = await guild.query_members(limit=1, user_ids=[member_id], cache=True)
    if not members:
        return None
    return members[0]
