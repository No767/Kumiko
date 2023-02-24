from typing import Dict, Union

from kumiko_cache import KumikoCache, commandKeyBuilder
from kumiko_utils import KumikoCM

from .models import KumikoServer


class KumikoServerCacheUtils:
    """Caching utils used in Kumiko's servers models"""

    def __init__(self, uri: str, models: list, redis_host: str, redis_port: int):
        """Caching utils used in Kumiko's servers models

        Args:
            uri (str): Connection URI
            models (list): List of Tortoise ORM models
            redis_host (str): Redis Host
            redis_port (int): Redis Port
        """
        self.self = self
        self.uri = uri
        self.models = models
        self.redis_host = redis_host
        self.redis_port = redis_port
        self.cache = KumikoCache(host=self.redis_host, port=self.redis_port)

    async def cacheServer(self, guild_id: int, command_name: str) -> Union[Dict, None]:
        """Abstraction for caching server configs

        The purpose of this is a helper coroutine that caches the guild data if not cached.
        If cached, it will return the cached data.

        Args:
            guild_id (int): Discord Guild ID
            command_name (str): Command Name. Will be used to set up the key on Redis

        Returns:
            Union[Dict, None]: This will return the cached data if cached, else it will return the data from the DB.
            Or in the case the user is not found, it will return None.
        """
        key = commandKeyBuilder(
            prefix="cache",
            namespace="kumiko",
            id=guild_id,
            command=f"{command_name}".replace(" ", "-"),
        )
        if await self.cache.cacheExists(key=key) is False:
            async with KumikoCM(uri=self.uri, models=self.models):
                serverData = (
                    await KumikoServer.filter(id=guild_id).get_or_none().values()
                )
                if serverData is None:
                    return None
                await self.cache.setDictCommandCache(key=key, value=serverData, ttl=15)
                return serverData
        else:
            return await self.cache.getDictCommandCache(key=key)
