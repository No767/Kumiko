from typing import Optional

import asyncpg
import discord
from redis.asyncio.connection import ConnectionPool

from .cache import GuildCacheHandler
from .structs import FullGuildConfig, GuildConfig, LoggingGuildConfig


async def get_or_fetch_full_config(
    guild_id: int, pool: asyncpg.Pool, redis_pool: ConnectionPool
) -> Optional[FullGuildConfig]:
    """Obtains the full config either from Redis or PostgreSQL

    Args:
        guild_id (int): Guild ID
        pool (asyncpg.Pool): Asyncpg connection pool
        redis_pool (ConnectionPool): Redis connection pool

    Returns:
        Optional[FullGuildConfig]: Config if found, None otherwise
    """
    query = """
        SELECT (
                guild.logs, 
                guild.local_economy, 
                guild.redirects, 
                guild.pins
            ) AS config,
            ( 
                logging_config.mod,
                logging_config.eco,
                logging_config.redirects
            ) AS logging
        FROM guild
        INNER JOIN logging_config ON guild.id = logging_config.guild_id
        WHERE guild.id = $1;
        """
    cache = GuildCacheHandler(guild_id, redis_pool)

    config = await cache.get_config()
    if config is not None:
        return config

    rows = await pool.fetchrow(query, guild_id)

    if rows is None:
        return None

    records = dict(rows)
    new_config = FullGuildConfig(
        config=GuildConfig(*records["config"]),
        logging_config=LoggingGuildConfig(*records["logging"]),
    )
    await cache.replace_full_config(new_config)
    return new_config


async def pull_and_add_cache(
    guild_id: int, conn: asyncpg.connection.Connection, redis_pool: ConnectionPool
):
    query = """
        SELECT (
                guild.logs, 
                guild.local_economy, 
                guild.redirects, 
                guild.pins
            ) AS config,
            (
                logging_config.mod,
                logging_config.eco,
                logging_config.redirects
            ) AS logging
        FROM guild
        INNER JOIN logging_config ON guild.id = logging_config.guild_id
        WHERE guild.id = $1;
        """
    cache = GuildCacheHandler(guild_id, redis_pool)
    rows = await conn.fetchrow(query, guild_id)

    if rows is None:
        await cache.invalidate()
        return None

    records = dict(rows)
    new_config = FullGuildConfig(
        config=GuildConfig(*records["config"]),
        logging_config=LoggingGuildConfig(*records["logging"]),
    )
    await cache.replace_full_config(new_config)
    return new_config


async def handle_guild_data(
    guild: discord.Guild,
    conn: asyncpg.connection.Connection,
    redis_pool: ConnectionPool,
):
    guild_id = guild.id
    cache = GuildCacheHandler(guild.id, redis_pool)
    exists = await cache.is_there()
    if not exists:
        await pull_and_add_cache(guild_id, conn, redis_pool)
    else:
        await cache.invalidate()
        await pull_and_add_cache(guild_id, conn, redis_pool)
