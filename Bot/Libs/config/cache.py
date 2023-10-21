import re
from enum import Enum
from typing import Dict, TypeVar, Union

import msgspec
import redis.asyncio as redis
from redis.asyncio.connection import ConnectionPool

# from .utils import parse_json_key
from .structs import FullGuildConfig, GuildConfig, LoggingGuildConfig

T = TypeVar("T", str, int, bool, None)

ValueType = Union[str, bool, int, Dict]


class ConfigType(Enum):
    CONFIG = "config"
    LOGGING = "logging"


def parse_json_key(key: str) -> str:
    return re.sub(r"^[.]|^[\$]", "", key, re.IGNORECASE)


class GuildCacheHandler:
    """First-class interface for handling guild config caches"""

    def __init__(self, guild_id: int, redis_pool: ConnectionPool) -> None:
        self.redis_pool = redis_pool
        self.guild_id = guild_id
        self.key = f"cache:kumiko:{guild_id}:guild_config"

    async def _exists(self, client: redis.Redis, key: str) -> bool:
        key_exists = await client.exists(key) >= 1
        return True if key_exists else False

    async def cache_defaults(self) -> FullGuildConfig:
        """Cache the default settings

        Returns:
            FullGuildConfig: The default settings
        """
        config_set = FullGuildConfig(
            config=GuildConfig(id=self.guild_id),
            logging_config=LoggingGuildConfig(channel_id=None),
        )
        client: redis.Redis = redis.Redis(connection_pool=self.redis_pool)
        await client.json(encoder=msgspec.json, decoder=msgspec.json).set(name=self.key, path="$", obj=config_set)  # type: ignore
        return config_set

    async def get_config(self) -> Union[FullGuildConfig, None]:
        """Get a config. The guild id is supplied through the constructor

        Returns:
            Union[FullGuildConfig, None]: The full config, or None if not found.
        """
        client: redis.Redis = redis.Redis(connection_pool=self.redis_pool)
        if await self._exists(client, self.key) is False:
            return None
        json = await client.json(encoder=None, decoder=None).get(self.key)  # type: ignore
        return msgspec.json.decode(json, type=FullGuildConfig)

    async def get_value(self, path: str) -> ValueType:
        """Gets the value given the path

        Args:
            path (str): Path to the value. This is also the key of the value

        Returns:
            ValueType: The value.
        """
        client: redis.Redis = redis.Redis(connection_pool=self.redis_pool)

        json = await client.json(encoder=None, decoder=msgspec.json.decode).get(self.key, path)  # type: ignore
        if isinstance(json, float):
            return int(json)
        return json

    async def merge_value(self, path: str, value: T) -> None:
        client: redis.Redis = redis.Redis(connection_pool=self.redis_pool)
        await client.json(encoder=msgspec.json, decoder=msgspec.json).merge(name=self.key, path=path, obj=value)  # type: ignore

    async def replace_full_config(self, config: FullGuildConfig) -> None:
        client: redis.Redis = redis.Redis(connection_pool=self.redis_pool)
        await client.json(encoder=msgspec.json, decoder=msgspec.json).set(name=self.key, path="$", obj=config)  # type: ignore
        await client.expire(self.key, 3600, nx=True)
