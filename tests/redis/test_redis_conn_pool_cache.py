import sys
from pathlib import Path

import redis

path = Path(__file__).parents[2].joinpath("Bot")
sys.path.append(str(path))

from Libs.cache import MemoryCache
from redis.connection import ConnectionPool


def test_pool_mem_cache_add():
    connPool = ConnectionPool(max_connections=25)
    memCache = MemoryCache()
    memCache.add(key="conn1", value=connPool)
    assert isinstance(memCache.get(key="conn1"), ConnectionPool)  # nosec


def test_pool_mem_cache_delete():
    connPool = ConnectionPool(max_connections=25)
    memCache = MemoryCache()
    memCache.add(key="conn1", value=connPool)
    memCache.delete(key="conn1")
    assert memCache.get(key="conn1") is None  # nosec


def test_pool_mem_cache_set():
    connPool = ConnectionPool(max_connections=25)
    memCache = MemoryCache()
    memCache.set(key="conn2", value=connPool)
    memCache.set(key="conn1", value=connPool)
    assert (  # nosec
        memCache.get(key="conn1") is not None and memCache.get(key="conn2") is not None
    )


def test_pool_mem_integration():
    connPool = ConnectionPool(max_connections=25)
    memCache = MemoryCache()
    memCache.add(key="conn1", value=connPool)
    currPool = memCache.get(key="conn1")
    r = redis.Redis(connection_pool=currPool)
    r.set("foo", "bar")
    res = r.get("foo")
    r.close()
    assert res == b"bar"  # nosec
