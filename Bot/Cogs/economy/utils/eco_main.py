import os
from typing import Optional

import motor.motor_asyncio
from beanie import Document, init_beanie
from dotenv import load_dotenv

load_dotenv()
MongoDB_Password = os.getenv("MongoDB_Password")
Username = os.getenv("MongoDB_Username")
Server_IP = os.getenv("MongoDB_Server_IP")


class Marketplace(Document):
    name: str
    description: Optional[str] = None
    amount: int


class KumikoEcoUtils:
    def __init__(self):
        self.self = self

    async def ins(
        self,
        name: Optional[str] = None,
        description: Optional[str] = None,
        amount: Optional[int] = None,
    ):
        client = motor.motor_asyncio.AsyncIOMotorClient(
            f"mongodb://{Username}:{MongoDB_Password}@{Server_IP}:27017"
        )
        await init_beanie(
            database=client.kumiko_marketplace, document_models=[Marketplace]
        )
        entry = Marketplace(name=name, description=description, amount=amount)
        await entry.insert()

    async def update(
        self,
        name: Optional[str] = None,
        description: Optional[str] = None,
        amount: Optional[int] = None,
    ):
        clientUpdate = motor.motor_asyncio.AsyncIOMotorClient(
            f"mongodb://{Username}:{MongoDB_Password}@{Server_IP}:27017"
        )
        await init_beanie(
            database=clientUpdate.kumiko_marketplace, document_models=[
                Marketplace]
        )
        entryUpdate = Marketplace(
            name=name, description=description, amount=amount)
        await entryUpdate.save()
