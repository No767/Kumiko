from typing import Any, Dict, Optional, Union

import msgspec
import redis.asyncio as redis
from redis.asyncio.connection import ConnectionPool

from .key_builder import command_key_builder


class KumikoCache:
    """Kumiko's custom caching library. Uses Redis as the backend."""

    def __init__(self, connection_pool: ConnectionPool) -> None:
        self.connection_pool = connection_pool

    async def set_basic_cache(
        self,
        key: Optional[str],
        value: Union[str, bytes] = "",
        ttl: Optional[int] = 30,
    ) -> None:
        """Sets the command cache on Redis
        Args:
            key (Optional[str], optional): Key to set on Redis. Defaults to `command_key_builder(prefix="cache", namespace="kumiko", user_id=None, command=None)`.
            value (Union[str, bytes, dict]): Value to set on Redis. Defaults to None.
            ttl (Optional[int], optional): TTL for the key-value pair. Defaults to 30.
        """
        default_key = command_key_builder(
            prefix="cache", namespace="kumiko", id=None, command=None
        )
        conn: redis.Redis = redis.Redis(connection_pool=self.connection_pool)
        await conn.set(
            name=key if key is not None else default_key, value=value, ex=ttl
        )

    async def get_basic_cache(self, key: str) -> Union[str, None]:
        """Gets the command cache from Redis

        Args:
            key (str): Key to get from Redis
        """
        conn: redis.Redis = redis.Redis(connection_pool=self.connection_pool)
        res = await conn.get(key)
        return res

    async def delete_basic_cache(self, key: str) -> None:
        """Deletes the command cache from Redis

        Args:
            key (str): Key to use
        """
        conn: redis.Redis = redis.Redis(connection_pool=self.connection_pool)
        await conn.delete(key)

    async def set_json_cache(
        self,
        key: str,
        value: Union[Dict[str, Any], Any],
        path: str = "$",
        ttl: Union[int, None] = None,
    ) -> None:
        """Sets the JSON cache on Redis

        Args:
            key (str): The key to use for Redis
            value (Union[Dict[str, Any], Any]): The value of the key-pair value
            path (str): The path to look for or set. Defaults to "$"
            ttl (Union[int, None], optional): TTL of the key-value pair. If None, then the TTL will not be set. Defaults to None.
        """
        client: redis.Redis = redis.Redis(connection_pool=self.connection_pool)
        await client.json(encoder=msgspec.json, decoder=msgspec.json).set(  # type: ignore # Assigning it the msgspec json encoders do work.
            name=key, path=path, obj=value
        )
        if isinstance(ttl, int):
            await client.expire(name=key, time=ttl)

    # The output type comes from here: https://github.com/redis/redis-py/blob/9f503578d1ffed20d63e8023bcd8a7dccd15ecc5/redis/commands/json/_util.py#L3C1-L3C73
    async def get_json_cache(
        self, key: str, path: str = "$", value_only: bool = True
    ) -> Union[None, Dict[str, Any], Any]:
        """Gets the JSON cache on Redis

        Args:
            key (str): The key of the key-value pair to get
            path (str): The path to obtain the value from. Defaults to "$" (aka the root)
            value_only (bool): Whether to return the value only. This is really only useful when using root paths. Defaults to True

        Returns:
            Dict[str, Any]: The value of the key-value pair
        """
        client: redis.Redis = redis.Redis(connection_pool=self.connection_pool)
        # Then again we know this works and redis-py 5.0 just broke things
        value = await client.json(encoder=msgspec.json, decoder=msgspec.json).get(  # type: ignore
            key, path
        )
        if value is None:
            return None
        if value_only is True:
            return value[0] if isinstance(value, list) else value
        return value

    async def delete_json_cache(self, key: str, path: str = "$") -> None:
        """Deletes the JSON cache at key `key` and under `path`

        Args:
            key (str): The key to use in Redis
            path (str): The path to look for. Defaults to "$" (root)
        """
        client: redis.Redis = redis.Redis(connection_pool=self.connection_pool)
        # With the upgrade to 5.0, they made it where the return value is an int
        # this basically breaks things
        await client.json().delete(key=key, path=path)  # type: ignore

    async def merge_json_cache(
        self,
        key: str,
        value: Union[Dict, Any],
        path: str = "$",
        ttl: Union[int, None] = None,
    ) -> None:
        """Merges the key and value into a new value

        This is the fix from using set_json_cache all of the time

        Args:
            key (str): Key to look for
            value (Union[Dict, Any]): Value to update
            path (str): The path to update. Defaults to "$"
            ttl (int): TTL. Usually leave this for perma cache. Defaults to None.
        """
        client: redis.Redis = redis.Redis(connection_pool=self.connection_pool)
        # Then again we know this works and redis-py 5.0 just broke things
        await client.json(encoder=msgspec.json, decoder=msgspec.json).merge(
            name=key, path=path, obj=value
        )  # type: ignore
        if isinstance(ttl, int):
            await client.expire(name=key, time=ttl)

    async def cache_exists(self, key: str) -> bool:
        """Checks to make sure if the cache exists

        Args:
            key (str): Redis key to check

        Returns:
            bool: Whether the key exists or not
        """
        client: redis.Redis = redis.Redis(connection_pool=self.connection_pool)
        key_exists = await client.exists(key) >= 1
        return True if key_exists else False
