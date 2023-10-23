import re
from enum import Enum
from typing import Dict, TypeVar, Union

import msgspec
import redis.asyncio as redis
from redis.asyncio.connection import ConnectionPool

from .structs import FullGuildConfig, GuildConfig, LoggingGuildConfig

T = TypeVar("T", str, bool, None)


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

    async def is_there(self):
        client: redis.Redis = redis.Redis(connection_pool=self.redis_pool)
        key_exists = await client.exists(self.key) >= 1
        return True if key_exists else False

    async def invalidate(self):
        client: redis.Redis = redis.Redis(connection_pool=self.redis_pool)
        await client.delete(self.key)

    async def cache_defaults(self) -> FullGuildConfig:
        """Cache the default settings

        Returns:
            FullGuildConfig: The default settings
        """
        config_set = FullGuildConfig(
            config=GuildConfig(),
            logging_config=LoggingGuildConfig(),
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

    async def get_value(self, path: str) -> Union[str, bool, Dict]:
        """Gets the value given the path

        Args:
            path (str): Path to the value. This is also the key of the value

        Returns:
            Union[str, bool, Dict]: The returned value from cache.
        """
        client: redis.Redis = redis.Redis(connection_pool=self.redis_pool)

        json = await client.json(encoder=..., decoder=...).get(self.key, path)  # type: ignore
        decoded = msgspec.json.decode(json)
        return decoded

    async def merge_value(self, path: str, value: Union[str, bool, None]) -> None:
        """Merge (aka replace) the value at the given path

        Args:
            path (str): Path to the value (aka the key)
            value (Union[str, bool, None]): New value to merge
        """
        client: redis.Redis = redis.Redis(connection_pool=self.redis_pool)
        await client.json(encoder=msgspec.json, decoder=msgspec.json).merge(name=self.key, path=path, obj=value)  # type: ignore

    async def replace_config(
        self, path: str, value: Union[GuildConfig, LoggingGuildConfig]
    ) -> None:
        client: redis.Redis = redis.Redis(connection_pool=self.redis_pool)
        await client.json(encoder=msgspec.json, decoder=msgspec.json).merge(name=self.key, path=path, obj=value)  # type: ignore

    async def replace_full_config(self, config: FullGuildConfig) -> None:
        """Replace the whole entire cache with a new config

        Args:
            config (FullGuildConfig): New config
        """
        client: redis.Redis = redis.Redis(connection_pool=self.redis_pool)
        await client.json(encoder=msgspec.json, decoder=msgspec.json).set(name=self.key, path="$", obj=config)  # type: ignore
