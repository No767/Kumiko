from typing import Union

import asyncpg
import discord
from discord.ext import commands
from Libs.cache import KumikoCache
from redis.asyncio.connection import ConnectionPool


async def get_or_fetch_status(
    guild_id: int, pool: asyncpg.Pool, redis_pool: ConnectionPool
) -> Union[bool, None]:
    sql = """
    SELECT redirects
    FROM guild
    WHERE id = $1;
    """
    key = f"cache:kumiko:{guild_id}:guild_config"
    cache = KumikoCache(connection_pool=redis_pool)
    if await cache.cache_exists(key=key):
        status = await cache.get_json_cache(
            key=key, path=".redirects", value_only=False
        )
        return status  # type: ignore
    else:
        value = await pool.fetchval(sql, guild_id)
        if value is None:
            return None
        await cache.merge_json_cache(key=key, value=value, path="$.redirects", ttl=None)
        return value


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
