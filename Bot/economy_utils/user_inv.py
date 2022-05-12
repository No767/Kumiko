import asyncio
import os
from typing import Optional

import motor.motor_asyncio
import uvloop
from beanie import Document, init_beanie
from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv()
MongoDB_Password = os.getenv("MongoDB_Password")
Username = os.getenv("MongoDB_Username")
Server_IP = os.getenv("MongoDB_Server_IP")


class Item(BaseModel):
    name: str
    description: Optional[str] = None
    amount: int


class User_Inventory(Document):
    user_id: int
    item: Item


class UsersInv:
    def __init__(self):
        self.self = self

    async def insItem(self, user_id: int, item: dict):
        client = motor.motor_asyncio.AsyncIOMotorClient(
            f"mongodb://{Username}:{MongoDB_Password}@{Server_IP}:27017"
        )
        await init_beanie(
            database=client.kumiko_user_inv, document_models=[User_Inventory]
        )
        entry = User_Inventory(user_id=user_id, item=item)
        await entry.create()

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    async def obtainInv(self, discord_user_id: int):
        clientObtainInv = motor.motor_asyncio.AsyncIOMotorClient(
            f"mongodb://{Username}:{MongoDB_Password}@{Server_IP}:27017"
        )
        await init_beanie(
            database=clientObtainInv.kumiko_user_inv,
            document_models=[User_Inventory],
        )
        results = await User_Inventory.find_many(
            User_Inventory.user_id == discord_user_id
        ).to_list()
        return results

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
