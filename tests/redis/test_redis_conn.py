import sys
from pathlib import Path

import pytest
from redis.asyncio.connection import ConnectionPool

path = Path(__file__).parents[2].joinpath("Bot")
sys.path.append(str(path))

from Libs.cache import MemoryCache
from Libs.utils.redis import pingRedis, redisCheck


@pytest.mark.asyncio
async def test_redis_ping():
    memCache = MemoryCache()
    memCache.add(
        key="main", value=ConnectionPool().from_url("redis://localhost:6379/0")
    )
    connPool = memCache.get(key="main")
    res = await pingRedis(connection_pool=connPool)
    assert res is True  # nosec


@pytest.mark.asyncio
async def test_redis_check():
    res = await redisCheck()
    assert res is True  # nosec
