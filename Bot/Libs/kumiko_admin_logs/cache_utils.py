from typing import List

from kumiko_cache import KumikoCache, commandKeyBuilder
from kumiko_utils import KumikoCM

from .models import KumikoAdminLogs


class KumikoAdminLogsCacheUtils:
    """Caching utils used in Kumiko's AL feature"""

    def __init__(self, uri: str, models: list, redis_host: str, redis_port: int):
        """Caching utils used in Kumiko's AL feature

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

    async def cacheAdminLogsView(
        self, guild_id: int, action: str, command_name: str
    ) -> List:
        """Abstraction for caching admin logs views

        The purpose of this is a helper coroutine that caches the guild data if not cached.
        If cached, it will return the cached data.

        Args:
            guild_id (int): Discord Guild ID
            action (str): Action of the admin logs. Bans, Timeouts, etc.
            command_name (str): Command Name. Will be used to set up the key on Redis

        Returns:
            List: The list of all of the data needed
        """
        key = commandKeyBuilder(
            prefix="cache",
            namespace="kumiko",
            id=guild_id,
            command=f"{command_name}".replace(" ", "-"),
        )
        if await self.cache.cacheExists(key=key) is False:
            async with KumikoCM(uri=self.uri, models=self.models):
                adminLogsData = (
                    await KumikoAdminLogs.filter(guild_id=guild_id).values()
                    if action.lower() == "all"
                    else await KumikoAdminLogs.filter(
                        guild_id=guild_id, action=action
                    ).values()
                )
                await self.cache.setBasicCommandCache(
                    key=key, value=adminLogsData, ttl=3
                )
                return adminLogsData
        else:
            return await self.cache.getBasicCommandCache(key=key)
