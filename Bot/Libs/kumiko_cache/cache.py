from typing import Dict, Optional, Union

import orjson
from coredis import Redis

from .key_builder import commandKeyBuilder


class KumikoCache:
    """Kumiko's custom caching library. Uses Redis as the backend."""

    def __init__(self, host: str = "127.0.0.1", port: int = 6379) -> None:
        """Kumiko's custom caching library. Uses Redis as the backend.

        Args:
            host (str, optional): Redis Server Host. Defaults to "127.0.0.1".
            port (int, optional): Redis Server Port. Defaults to 6379.
        """
        self.self = self
        self.host = host
        self.port = port

    async def setBasicCommandCache(
        self,
        key: Optional[str] = commandKeyBuilder(
            prefix="cache", namespace="akari", id=None, command=None
        ),
        value: Union[str, bytes, dict] = None,
        ttl: Optional[int] = 30,
    ) -> None:
        """Sets the command cache on Redis
        Args:
            key (Optional[str], optional): Key to set on Redis. Defaults to `commandKeyBuilder(prefix="akari", namespace="cache", user_id=None, command=None)`.
            value (Union[str, bytes, dict]): Value to set on Redis. Defaults to None.
            ttl (Optional[int], optional): TTL for the key-value pair. Defaults to 30.
        """
        conn = Redis(host=self.host, port=self.port, decode_responses=True)
        await conn.set(key=key, value=orjson.dumps(value), ex=ttl)

    async def getBasicCommandCache(self, key: str) -> str:
        """Gets the command cache from Redis
        Args:
            key (str): Key to get from Redis
        """
        conn = Redis(host=self.host, port=self.port, decode_responses=True)
        return orjson.loads(await conn.get(key))

    async def setDictCommandCache(
        self,
        key: Optional[str] = commandKeyBuilder(
            prefix="cache", namespace="akari", id=None, command=None
        ),
        value: Dict = None,
        ttl: Optional[int] = 30,
    ) -> None:
        """Sets the command cache using hashes on Redis

        Args:
            key (Optional[str], optional): Key to set on Redis. Defaults to commandKeyBuilder( prefix="cache", namespace="akari", id=None, command=None ).
            value (Dict): The dict to set on Redis. This will get converted to a hash. Defaults to None.
            ttl (Optional[int], optional): How long the key-value pair lasts for. Defaults to 30 (seconds).
        """
        conn = Redis(host=self.host, port=self.port, decode_responses=True)
        await conn.hset(key=key, field_values=value)
        await conn.expire(key=key, seconds=ttl)

    async def getDictCommandCache(self, key: str):
        """Gets the command cache from Redis

        Args:
            key (str): Key to get from Redis
        """
        conn = Redis(host=self.host, port=self.port, decode_responses=True)
        return await conn.hgetall(key=key)

    async def cacheExists(self, key: str) -> bool:
        """Checks if the key exists or not
        Args:
            key (str): The key to check against
        Returns:
            bool: If the key exists or not
        """
        conn = Redis(host=self.host, port=self.port)
        data = await conn.exists([key])
        return True if data >= 1 else False
