from typing import Dict, List, Union

import simdjson
from kumiko_cache import KumikoCache, commandKeyBuilder
from tortoise.contrib.pydantic import pydantic_model_creator, pydantic_queryset_creator

from .models import EcoMarketplace, EcoUser


class KumikoEconomyCacheUtils:
    """Cache utilities used by Kumiko for her economy system"""

    def __init__(self, uri: str, models: List, redis_host: str, redis_port: int):
        self.self = self
        self.uri = uri
        self.models = models
        self.redis_host = redis_host
        self.redis_port = redis_port
        self.cache = KumikoCache(connection_pool=None, host=redis_host, port=redis_port)

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
            pydanticUserBridgeData = pydantic_model_creator(EcoUser)
            userData = await EcoUser.filter(user_id=user_id).get_or_none()
            if userData is None:
                return None
            userS = await pydanticUserBridgeData.from_tortoise_orm(userData)
            await self.cache.setBasicCommandCache(key=key, value=userS.json(), ttl=15)
            return userS.dict()
        else:
            jsonParser = simdjson.Parser()
            return jsonParser.parse(
                await self.cache.getBasicCommandCache(key=key), recursive=True
            )

    async def cacheMarketplace(
        self, user_id: int, command_name: str
    ) -> Union[Dict, None]:
        """The abstraction layer for caching the requested user's data

        The purpose of this is a helper coroutine that caches the guild data if not cached.
        If cached, it will return the cached data.

        Args:
            user_id (int): Discord User ID
            command_name (str):

        Returns:
            Union[Dict, None]: _description_
        """
        key = commandKeyBuilder(
            prefix="cache",
            namespace="kumiko",
            id=user_id,
            command=f"{command_name}".replace(" ", "-"),
        )
        jsonParser = simdjson.Parser()
        if await self.cache.cacheExists(key=key) is False:
            pydanticMarketplaceData = pydantic_queryset_creator(EcoMarketplace)
            marketplaceS = await pydanticMarketplaceData.from_queryset(
                EcoMarketplace.all().limit(25)
            )
            mJson = marketplaceS.json()
            parsedData = jsonParser.parse(mJson, recursive=True)
            await self.cache.setBasicCommandCache(key=key, value=mJson, ttl=15)
            return parsedData
        else:
            return jsonParser.parse(
                await self.cache.getBasicCommandCache(key=key), recursive=True
            )
