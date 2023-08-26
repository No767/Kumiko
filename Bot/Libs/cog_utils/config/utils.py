import asyncpg
from Libs.cache import KumikoCache
from redis.asyncio.connection import ConnectionPool


async def configure_settings(
    status: bool,
    value: str,
    guild_id: int,
    pool: asyncpg.Pool,
    redis_pool: ConnectionPool,
) -> str:
    """Configure the settings"""
    key = f"cache:kumiko:{guild_id}:guild_config"
    cache = KumikoCache(redis_pool)
    str_status = "Enabled" if status is True else "Disabled"
    return_status = f"{str_status} {value}"

    if value in "EventsLog":
        query = """
        UPDATE guild
        SET logs = $2
        WHERE id = $1;
        """
        await pool.execute(query, guild_id, status)
        await cache.merge_json_cache(key=key, value=status, path=".logs")
        if status is False:
            await cache.merge_json_cache(
                key=key, value=None, path=".logging_config.channel_id"
            )
        return return_status

    query = """
    UPDATE guild
    SET local_economy = $2
    WHERE id = $1;
    """
    json_path = ".local_economy"

    if value in "Redirects":
        query = """
        UPDATE guild
        SET redirects = $2
        WHERE id = $1;
        """
        json_path = ".redirects"
    elif value in "Pins":
        query = """
        UPDATE guild
        SET pins = $2
        WHERE id = $1;
        """
        json_path = ".pins"

    await pool.execute(query, guild_id, status)
    await cache.merge_json_cache(key=key, value=status, path=json_path)
    return return_status


async def check_already_set(
    value: str, guild_id: int, redis_pool: ConnectionPool
) -> bool:
    """Checks to make sure that the feature is enabled/disabled before setting it up

    Args:
        value (str): Feature to check
        guild_id (int): Guild ID
        redis_pool (ConnectionPool): Redis Connection Pool

    Returns:
        bool: True if the existing feature is enabled, False if not
    """
    value_to_key = {
        "Economy": ".local_economy",
        "Redirects": ".redirects",
        "EventsLog": ".logs",
        "Pins": ".pins",
    }
    key = f"cache:kumiko:{guild_id}:guild_config"
    cache = KumikoCache(redis_pool)
    json_path = (
        value_to_key["Economy"]
        if value in ["Economy", "Marketplace", "Jobs", "Auctions"]
        else value_to_key[value]
    )
    res = await cache.get_json_cache(key=key, path=json_path, value_only=False)
    if res is True:
        return True
    return False
