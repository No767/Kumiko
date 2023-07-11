from typing import Any, Dict, Union

import asyncpg
from Libs.cache import KumikoCache, cacheJson
from redis.asyncio.connection import ConnectionPool


# idk how to test this one
# Someone remind Noelle to test this once she figures out how to
@cacheJson(ttl=None, name="logging_config")
async def get_or_fetch_config(
    id: int, redis_pool: ConnectionPool, pool: asyncpg.Pool
) -> Union[Dict[str, Union[int, bool]], None]:
    query = """
    SELECT guild.id, guild.logs, logging_config.channel_id, logging_config.member_events
    FROM guild
    INNER JOIN logging_config
    ON guild.id = logging_config.guild_id
    WHERE guild.id = $1;
    """
    async with pool.acquire() as conn:
        res = await conn.fetchrow(query, id)
        return dict(res)


async def set_or_update_cache(
    key: str, redis_pool: ConnectionPool, data: Dict[str, Any]
) -> None:
    cache = KumikoCache(connection_pool=redis_pool)
    if not await cache.cacheExists(key=key):
        await cache.setJSONCache(key=key, value=data, ttl=None)
    else:
        await cache.setJSONCache(
            key=key, value=data["channel_id"], path="$.channel_id", ttl=None
        )


async def delete_cache(key: str, redis_pool: ConnectionPool) -> None:
    cache = KumikoCache(connection_pool=redis_pool)
    if await cache.cacheExists(key=key):
        await cache.deleteJSONCache(key=key)
