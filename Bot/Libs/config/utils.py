import asyncpg
from Libs.cache import KumikoCache
from Libs.config import GuildConfig, LoggingGuildConfig
from redis.asyncio.connection import ConnectionPool


async def get_or_fetch_guild_config(
    guild_id: int, pool: asyncpg.Pool, redis_pool: ConnectionPool
):
    sql = """
    SELECT guild.id, logging_config.channel_id,  logging_config.mod_events, logging_config.mod_events, logging_config.eco_events, guild.logs, guild.birthday, guild.pins, guild.redirects, guild.local_economy, guild.local_economy_name
    FROM guild
    INNER JOIN logging_config
    ON guild.id = logging_config.guild_id
    WHERE guild.id = $1;
    """
    key = f"cache:kumiko:{guild_id}:guild_config"
    cache = KumikoCache(connection_pool=redis_pool)
    if await cache.cache_exists(key=key):
        res = await cache.get_json_cache(key=key, path="$")
        return res
    rows = await pool.fetchrow(sql, guild_id)
    if rows is None:
        return None
    fetched_rows = dict(rows)
    guild_config = GuildConfig(
        id=fetched_rows["id"],
        logging_config=LoggingGuildConfig(
            channel_id=fetched_rows["channel_id"],
            mod_events=fetched_rows["mod_events"],
            eco_events=fetched_rows["eco_events"],
        ),
        logs=fetched_rows["logs"],
        birthday=fetched_rows["birthday"],
        pins=fetched_rows["pins"],
        redirects=fetched_rows["redirects"],
        local_economy=fetched_rows["local_economy"],
        local_economy_name=fetched_rows["local_economy_name"],
    )
    await cache.set_json_cache(key=key, value=guild_config, path="$", ttl=None)
    return fetched_rows
