import asyncio
import os
from typing import Union

import asyncpg
import uvloop
from dotenv import load_dotenv
from Libs.cache import cacheJson
from pyinstrument import Profiler
from redis.asyncio.connection import ConnectionPool

profiler = Profiler()

load_dotenv()

POSTGRES_URI = os.environ["POSTGRES_URI"]

profiler.start()


@cacheJson(ttl=None)
async def get_or_fetch_config(
    id: int, redis_pool: ConnectionPool, pool: asyncpg.Pool
) -> Union[dict, None]:
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


async def main():
    # r: redis.Redis = redis.Redis(decode_responses=True)
    # await r.hset(name="test", mapping={"testMore": int(True), "testSomeMore": int(False)})
    # # res = await r.hgetall(name="test")
    # # print(bool(True))
    # # print(res)
    # # print(type(res))
    # key = "test"
    # print(await r.exists(key))
    async with asyncpg.create_pool(dsn=POSTGRES_URI) as pool:
        res = await get_or_fetch_config(
            id=970159505390325842,
            redis_pool=ConnectionPool(decode_responses=True),
            pool=pool,
        )
        print(res["id"])


if __name__ == "__main__":
    uvloop.install()
    asyncio.run(main())
    profiler.stop()
    profiler.print()
