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
    kumikoCP = KumikoCPManager(uri=REDIS_URI)
    connPool = kumikoCP.createPool()
    assert isinstance(connPool, ConnectionPool)


def test_get_cp():
    kumikoCP = KumikoCPManager(uri=REDIS_URI)
    connPool = kumikoCP.getConnPool()
    assert isinstance(connPool, ConnectionPool)
