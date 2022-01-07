import os

import motor.motor_asyncio
from dotenv import load_dotenv

load_dotenv()

Password = os.getenv("MongoDB_Password")
Username = os.getenv("MongoDB_Username")
Server_IP = os.getenv("MongoDB_Server_IP")


# Note: All of these methods are coroutines. They are not regular methods


class ecoBase:
    def __init__(self, ctx):
        self.id = ctx.author.id
        self.gid = ctx.guild.id

    async def get_amount(self):
        client = motor.motor_asyncio.AsyncIOMotorClient(
            f"mongodb://{Username}:{Password}@{Server_IP}:27017"
        )
        db = client.kumiko_economy
        user_data = {"user.discord_id": {"$eq": self.id},
                     "user.gid": {"$eq": self.gid}}
        eco = db["kumiko_eco"]
        finder = await eco.find_one(user_data)
        if finder is None:
            user_data_insert = {
                "user": {"discord_id": self.id, "gid": self.gid, "coins": 0}
            }
            eco.insert_one(user_data_insert)
        else:
            return finder

    async def set_amount(self, coins):
        setter_client = motor.motor_asyncio.AsyncIOMotorClient(
            f"mongodb://{Username}:{Password}@{Server_IP}:27017"
        )
        database = setter_client.kumiko_economy
        kumiko_eco = database["kumiko_eco"]
        await kumiko_eco.update_one(
            {"user.discord_id": {"$eq": self.id}, "user.gid": {"$eq": self.gid}},
            {"$set": {"user.coins": coins}},
        )
