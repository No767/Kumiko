import sys
from pathlib import Path

import pytest
from redis.asyncio.connection import ConnectionPool

path = Path(__file__).parents[2].joinpath("Bot")
sys.path.append(str(path))

from Libs.cache import KumikoCache
from Libs.cog_utils.events_log import set_or_update_cache


@pytest.fixture(scope="session")
def get_data():
    return {"id": 123, "channel_id": 2342634575000}


@pytest.mark.asyncio
async def test_set_or_update_cache(get_data):
    connPool = ConnectionPool()
    key = "cache:kumiko:123:config"
    cache = KumikoCache(connPool)
    await set_or_update_cache(key=key, redis_pool=connPool, data=get_data)
    res = await cache.getJSONCache(key=key)
    assert res[0] == get_data  # type: ignore


@pytest.mark.asyncio
async def test_cached_set_or_update(get_data):
    connPool = ConnectionPool()
    key = "cache:kumiko:1234:config"
    cache = KumikoCache(connPool)
    res = await cache.setJSONCache(key=key, value=get_data)
    await set_or_update_cache(key=key, redis_pool=connPool, data=get_data)
    res = await cache.getJSONCache(key=key)
    assert res[0] == get_data and res[0]["channel_id"] == get_data["channel_id"]  # type: ignore
