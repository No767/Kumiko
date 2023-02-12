from datetime import datetime
from typing import Union

import ciso8601
from coredis import ConnectionPool, Redis


def parseDatetime(datetime: Union[datetime, str]) -> datetime:
    """Parses a datetime object or a string into a datetime object

    Args:
        datetime (Union[datetime.datetime, str]): Datetime object or string to parse

    Returns:
        datetime.datetime: Parsed datetime object
    """
    if isinstance(datetime, str):
        return ciso8601.parse_datetime(datetime)
    return datetime


async def pingRedis(connection_pool: ConnectionPool) -> bool:
    """Pings Redis to make sure it is alive

    Args:
        connection_pool (ConnectionPool): ConnectionPool object to use

    Returns:
        bool: Whether Redis is alive or not
    """
    r = Redis(connection_pool=connection_pool)
    res = await r.ping()
    return True if res == b"PONG" or b"HELLO" or "HELLO" or "PONG" else False
