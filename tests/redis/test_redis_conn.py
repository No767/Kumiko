import os
import sys
from pathlib import Path

import pytest
from aiocache import Cache
from coredis import ConnectionPool

path = Path(__file__).parents[2]
packagePath = os.path.join(str(path), "Bot", "Libs")
sys.path.append(packagePath)

from kumiko_utils import pingRedis
from kumiko_utils.redis import pingRedisServer, setupRedisConnPool


@pytest.fixture(autouse=True, scope="session")
def mem_cache():
    memCache = Cache()
    return memCache


@pytest.mark.asyncio
async def test_setup_redis_conn_pool(mem_cache):
    await setupRedisConnPool(mem_cache=mem_cache)
    getConnPool = await mem_cache.get("main")
    assert isinstance(getConnPool, ConnectionPool)  # nosec


@pytest.mark.asyncio
async def test_ping_redis_server(mem_cache):
    await mem_cache.add("main2", ConnectionPool().from_url("redis://localhost:6379/0"))
    getConnPool = await mem_cache.get("main2")
    res = await pingRedisServer(connection_pool=getConnPool)
    otherRes = await pingRedis(connection_pool=getConnPool)
    assert res is True and otherRes is True  # nosec
