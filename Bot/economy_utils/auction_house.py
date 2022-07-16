import os

import asyncio_redis
from dotenv import load_dotenv

load_dotenv()
REDIS_SERVER_IP = os.getenv("Redis_Server_IP_Dev")
REDIS_SERVER_PORT = os.getenv("Redis_Port_Dev")


class KumikoAuctionHouseUtils:
    def __init__(self):
        self.self = self

    async def getItemKey(self, key: str):
        """Gets the keys for an item within Redis

        Args:
            key (str): The key to get
        """
        conn = await asyncio_redis.Pool.create(
            host=REDIS_SERVER_IP, port=int(REDIS_SERVER_PORT)
        )
        getKey = await conn.get(key)
        conn.close()
        return getKey

    async def setItemKey(self, key: str, value: int):
        """Sets that key within Redis

        Args:
            key (str): The key to set
            value (int): The value to set
        """
        conn = await asyncio_redis.Pool.create(
            host=REDIS_SERVER_IP, port=int(REDIS_SERVER_PORT)
        )
        await conn.set(key, str(value))
        conn.close()
