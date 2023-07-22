import asyncpg
from attrs import asdict
from Libs.cache import KumikoCache
from Libs.config import GuildConfig, LoggingGuildConfig
from redis.asyncio.connection import ConnectionPool


async def get_or_fetch_guild_config(
    guild_id: int, pool: asyncpg.Pool, redis_pool: ConnectionPool
):
    sql = """
    SELECT guild.id, guild.logs, guild.birthday, guild.local_economy, guild.local_economy_name, logging_config.channel_id, logging_config.member_events, logging_config.mod_events, logging_config.mod_events, logging_config.eco_events
    FROM guild
    INNER JOIN logging_config
    ON guild.id = logging_config.guild_id
    WHERE guild.id = $1;
    """
    key = f"cache:kumiko:{guild_id}:guild_config"
    cache = KumikoCache(connection_pool=redis_pool)
    if await cache.cacheExists(key=key):
        res = await cache.getJSONCache(key=key, path=".")
        print(res)
        return res
    rows = await pool.fetchrow(sql, guild_id)
    if rows is None:
        return None
    fetchedRows = dict(rows)
    guildConfig = GuildConfig(
        id=fetchedRows["id"],
        logging_config=LoggingGuildConfig(
            channel_id=fetchedRows["channel_id"],
            member_events=fetchedRows["member_events"],
            mod_events=fetchedRows["mod_events"],
            eco_events=fetchedRows["eco_events"],
        ),
        logs=fetchedRows["logs"],
        birthday=fetchedRows["birthday"],
        local_economy=fetchedRows["local_economy"],
        local_economy_name=fetchedRows["local_economy_name"],
    )
    await cache.setJSONCache(key=key, value=asdict(guildConfig), path=".", ttl=None)
    return asdict(guildConfig)
