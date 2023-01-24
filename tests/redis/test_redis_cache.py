import os
import sys
from pathlib import Path

import pytest
from aiocache import Cache
from coredis import ConnectionPool

path = Path(__file__).parents[2]
packagePath = os.path.join(str(path), "bot", "libs")
sys.path.append(packagePath)

from Bot.Libs.kumiko_cache import KumikoCache, commandKeyBuilder

DATA = "Hello World"


@pytest.mark.asyncio
async def test_basic_cache():
    key = commandKeyBuilder(id=None, command=None)
    connPool = ConnectionPool().from_url("redis://localhost:6379/0")
    cache = KumikoCache(connection_pool=connPool)
    await cache.setBasicCommandCache(key=key, value=DATA)
    res = await cache.getBasicCommandCache(key=key)
    assert (res == DATA) and (isinstance(res, str))  # nosec


@pytest.mark.asyncio
async def test_basic_cache_from_mem():
    key = commandKeyBuilder(id=None, command=None)
    connPool = ConnectionPool().from_url("redis://localhost:6379/0")
    memCache = Cache(Cache.MEMORY)
    await memCache.set("redis_conn_pool", connPool)
    getConnPool = await memCache.get("redis_conn_pool")
    if getConnPool is None:
        raise ValueError("Unable to get conn pool from mem cache")
    cache = KumikoCache(connection_pool=getConnPool)
    res = await cache.getBasicCommandCache(key=key)
    assert (res == DATA) and (isinstance(res, str))  # nosec
