import sys
from pathlib import Path

path = Path(__file__).parents[2].joinpath("Bot")
sys.path.append(str(path))

from Libs.cache import kumikoCP
from redis.asyncio.connection import ConnectionPool


def test_get_cp():
    connPool = kumikoCP.getConnPool()
    assert isinstance(connPool, ConnectionPool)


def test_creation_cp():
    connPool = kumikoCP.createConnPool()
    assert isinstance(connPool, ConnectionPool)
