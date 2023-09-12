from typing import Any, Dict, Union

import asyncpg
from Libs.cache import KumikoCache
from redis.asyncio.connection import ConnectionPool


async def get_or_fetch_config(
    id: int, redis_pool: ConnectionPool, pool: asyncpg.Pool
) -> Union[Dict[str, Union[int, bool]], None]:
    query = """
    SELECT logging_config.channel_id, logging_config.member_events, logging_config.eco_events
    FROM guild
    INNER JOIN logging_config
    ON guild.id = logging_config.guild_id
    WHERE guild.id = $1;
    """
    key = f"cache:kumiko:{id}:guild_config"
    cache = KumikoCache(redis_pool)
    if await cache.cache_exists(key=key):
        res = await cache.get_json_cache(key=key, path=".logging_config")
        return res
    else:
        rows = await pool.fetchrow(query, id)
        if rows is None:
            return None
        return dict(rows)


async def get_or_fetch_log_enabled(
    id: int, redis_pool: ConnectionPool, pool: asyncpg.Pool
) -> bool:
    query = """
    SELECT logs
    FROM guild
    WHERE id = $1;
    """
    key = f"cache:kumiko:{id}:guild_config"
    cache = KumikoCache(redis_pool)
    if await cache.cache_exists(key=key):
        res = await cache.get_json_cache(key=key, path=".logs", value_only=False)
        return res  # type: ignore
    else:
        val = await pool.fetchval(query, id)
        if val is None:
            return False
        return val


async def get_or_fetch_channel_id(
    guild_id: int, pool: asyncpg.Pool, redis_pool: ConnectionPool
) -> Union[str, None]:
    query = """
    SELECT logging_config.channel_id
    FROM logging_config
    WHERE guild_id = $1;
    """
    key = f"cache:kumiko:{guild_id}:logging_channel_id"
    cache = KumikoCache(redis_pool)
    if await cache.cache_exists(key=key):
        res = await cache.get_basic_cache(key=key)
        return res
    else:
        val = await pool.fetchval(query, guild_id)
        if val is None:
            return None
        await cache.set_basic_cache(key=key, value=val, ttl=3600)
        return val


async def set_or_update_cache(
    key: str, redis_pool: ConnectionPool, data: Dict[str, Any]
) -> None:
    cache = KumikoCache(connection_pool=redis_pool)
    if not await cache.cache_exists(key=key):
        await cache.set_json_cache(key=key, value=data, ttl=None)
    else:
        await cache.set_json_cache(
            key=key, value=data["channel_id"], path=".channel_id", ttl=None
        )


async def disable_logging(guild_id: int, redis_pool: ConnectionPool) -> None:
    key = f"cache:kumiko:{guild_id}:guild_config"
    cache = KumikoCache(connection_pool=redis_pool)
    await cache.delete_basic_cache(key=f"cache:kumiko:{guild_id}:logging_channel_id")
    await cache.merge_json_cache(key=key, value=False, path=".logs", ttl=None)
    await cache.merge_json_cache(
        key=key, value=None, path=".logging_config.channel_id", ttl=None
    )
