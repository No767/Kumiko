import sys
from pathlib import Path

path = Path(__file__).parents[2].joinpath("Bot")
sys.path.append(str(path))

import pytest
from Libs.cache import KumikoCPManager
from redis.asyncio.connection import ConnectionPool

REDIS_URI = "redis://localhost:6379/0"


@pytest.mark.asyncio
async def test_cpm():
    async with KumikoCPManager(uri=REDIS_URI) as cpm:
        assert isinstance(cpm, ConnectionPool)


def test_creation_cp():
    kumiko_cp = KumikoCPManager(uri=REDIS_URI)
    pool = kumiko_cp.create_pool()
    assert isinstance(pool, ConnectionPool)


def test_get_cp():
    kumiko_cp = KumikoCPManager(uri=REDIS_URI)
    pool = kumiko_cp.get_conn_pool()
    assert isinstance(pool, ConnectionPool)


def test_created_cp():
    kumiko_cp = KumikoCPManager(uri=REDIS_URI)
    kumiko_cp.create_pool()
    new_pool = kumiko_cp.get_conn_pool()
    assert isinstance(new_pool, ConnectionPool)
