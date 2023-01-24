import os
import sys
from pathlib import Path

import pytest
from aiocache import Cache
from coredis import ConnectionPool, Redis

path = Path(__file__).parents[2]
packagePath = os.path.join(str(path), "bot", "libs")
sys.path.append(packagePath)


@pytest.mark.asyncio
async def test_pool_mem_cache_add():
    connPool = ConnectionPool(max_connections=25)
    memCache = Cache(Cache.MEMORY)
    await memCache.add(key="conn1", value=connPool)
    assert isinstance(await memCache.get(key="conn1"), ConnectionPool)  # nosec


@pytest.mark.asyncio
async def test_pool_mem_cache_delete():
    connPool = ConnectionPool(max_connections=25)
    memCache = Cache(Cache.MEMORY)
    await memCache.add(key="conn1", value=connPool)
    await memCache.delete(key="conn1")
    assert await memCache.get(key="conn1") is None  # nosec


@pytest.mark.asyncio
async def test_pool_mem_cache_set():
    connPool = ConnectionPool(max_connections=25)
    memCache = Cache(Cache.MEMORY)
    await memCache.set(key="conn1", value=connPool)
    await memCache.set(key="conn2", value=connPool)
    assert (  # nosec
        await memCache.get(key="conn1") is not None
        and await memCache.get(key="conn2") is not None
    )


@pytest.mark.asyncio
async def test_pool_mem_integration():
    connPool = ConnectionPool(max_connections=25)
    memCache = Cache(Cache.MEMORY)
    await memCache.add(key="conn1", value=connPool)
    currPool = await memCache.get(key="conn1")
    r = Redis(connection_pool=currPool)
    await r.set("foo", "bar")
    res = await r.get("foo")
    await r.quit()
    assert res == b"bar"  # nosec
