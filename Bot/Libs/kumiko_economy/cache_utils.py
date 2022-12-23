from typing import Dict, List, Union

from kumiko_cache import KumikoCache, commandKeyBuilder
from kumiko_utils import KumikoCM
from tortoise.contrib.pydantic import pydantic_model_creator

from .models import EcoUser


class KumikoEconomyCacheUtils:
    """Cache utilities used by Kumiko for her economy system"""

    def __init__(self, uri: str, models: List, redis_host: str, redis_port: int):
        self.self = self
        self.uri = uri
        self.models = models
        self.redis_host = redis_host
        self.redis_port = redis_port
        self.cache = KumikoCache(host=redis_host, port=redis_port)

    async def cacheUser(self, user_id: int, command_name: str) -> Union[Dict, None]:
        """The abstraction layer for caching the requested user's data

        The purpose of this is a helper coroutine that caches the guild data if not cached.
        If cached, it will return the cached data.

        Args:
            user_id (int): Discord User ID
            command_name (str): _description_

        Returns:
            Union[Dict, None]: _description_
        """
        key = commandKeyBuilder(
            prefix="cache",
            namespace="kumiko",
            id=user_id,
            command=f"{command_name}".replace(" ", "-"),
        )
        if await self.cache.cacheExists(key=key) is False:
            async with KumikoCM(uri=self.uri, models=self.models):
                pydanticUserBridgeData = pydantic_model_creator(EcoUser)
                userData = await EcoUser.filter(user_id=user_id).get_or_none()
                if userData is None:
                    return None
                userS = await pydanticUserBridgeData.from_tortoise_orm(userData)
                userDictData = userS.dict()
                await self.cache.setBasicCommandCache(
                    key=key, value=userDictData, ttl=15
                )
                return userDictData
        else:
            return await self.cache.getBasicCommandCache(key=key)
