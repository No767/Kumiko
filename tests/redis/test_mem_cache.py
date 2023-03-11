import sys
from pathlib import Path

import pytest

path = Path(__file__).parents[2].joinpath("Bot")
sys.path.append(str(path))

from Libs.cache import MemoryCache
from redis.connection import ConnectionPool


@pytest.fixture(autouse=True, scope="session")
def load_conn_pool() -> ConnectionPool:
    return ConnectionPool().from_url("redis://localhost:6379/0")


def test_mem_cache_set(load_conn_pool):
    memCache = MemoryCache()
    memCache.set(key="main", value=load_conn_pool)
    res = memCache.get(key="main")
    assert isinstance(res, ConnectionPool)  # nosec


def test_mem_cache_add(load_conn_pool):
    memCache = MemoryCache()
    memCache.add(key="main4", value=load_conn_pool)
    res = memCache.get(key="main4")
    assert isinstance(res, ConnectionPool)  # nosec


def test_mem_cache_add_error(load_conn_pool):
    with pytest.raises(ValueError) as execinfo:
        memCache = MemoryCache()
        memCache.add(key="main", value=load_conn_pool)
        memCache.add(key="main", value=load_conn_pool)
    assert (  # nosec
        str(execinfo.value)
        == "Key main already exists. Please use .set to update it"  # nosec
    )  # nosec


def test_mem_cache_delete_return(load_conn_pool):
    memCache = MemoryCache()
    memCache.set(key="main3", value=load_conn_pool)
    res = memCache.delete(key="main3")
    assert isinstance(res, ConnectionPool)  # nosec


def test_mem_cache_delete(load_conn_pool):
    memCache = MemoryCache()
    memCache.set(key="main2", value=load_conn_pool)
    memCache.delete(key="main2")
    currCache = memCache.getAll()
    assert len(currCache) == 0  # nosec
