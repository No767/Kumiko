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


class Marketplace(Document):
    name: str
    description: Optional[str] = None
    amount: int
    price: int
    date_added: str
    owner: int


class ProjectOnlyID(BaseModel):
    owner: int


class KumikoEcoUtils:
    def __init__(self):
        self.self = self

    async def ins(
        self,
        date_added: str,
        owner: int,
        name: Optional[str] = None,
        description: Optional[str] = None,
        amount: Optional[int] = None,
        price: Optional[int] = None,
    ):
        client = motor.motor_asyncio.AsyncIOMotorClient(
            f"mongodb://{Username}:{MongoDB_Password}@{Server_IP}:27017"
        )
        await init_beanie(
            database=client.kumiko_marketplace, document_models=[Marketplace]
        )
        entry = Marketplace(
            name=name,
            description=description,
            amount=amount,
            price=price,
            date_added=date_added,
            owner=owner,
        )
        await entry.create()

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    async def update(
        self,
        date_added: str,
        owner: int,
        name: Optional[str] = None,
        description: Optional[str] = None,
        amount: Optional[int] = None,
        price: Optional[int] = None,
    ):
        clientUpdate = motor.motor_asyncio.AsyncIOMotorClient(
            f"mongodb://{Username}:{MongoDB_Password}@{Server_IP}:27017"
        )
        await init_beanie(
            database=clientUpdate.kumiko_marketplace, document_models=[Marketplace]
        )
        entryUpdate = Marketplace(
            name=name,
            description=description,
            amount=amount,
            price=price,
            date_added=date_added,
            owner=owner,
        )
        await entryUpdate.save()

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    async def obtain(self):
        clientObtain = motor.motor_asyncio.AsyncIOMotorClient(
            f"mongodb://{Username}:{MongoDB_Password}@{Server_IP}:27017"
        )
        await init_beanie(
            database=clientObtain.kumiko_marketplace, document_models=[Marketplace]
        )
        resMain = await Marketplace.find_all().to_list()
        return resMain

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    async def obtainOnlyID(self, owner_id: int):
        clientObtainOnlyID = motor.motor_asyncio.AsyncIOMotorClient(
            f"mongodb://{Username}:{MongoDB_Password}@{Server_IP}:27017"
        )
        await init_beanie(
            database=clientObtainOnlyID.kumiko_marketplace,
            document_models=[Marketplace],
        )
        resMain3 = await Marketplace.find_one(Marketplace.owner == owner_id).project(
            ProjectOnlyID
        )
        return resMain3

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    async def obtainOnlyIDWithName(self, name: str, owner_id: int):
        clientObtainOnlyIDWithName = motor.motor_asyncio.AsyncIOMotorClient(
            f"mongodb://{Username}:{MongoDB_Password}@{Server_IP}:27017"
        )
        await init_beanie(
            database=clientObtainOnlyIDWithName.kumiko_marketplace,
            document_models=[Marketplace],
        )
        resMain4 = await Marketplace.find_one(
            Marketplace.owner == owner_id, Marketplace.name == name
        ).project(ProjectOnlyID)
        return resMain4

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    async def getItem(self, name: str):
        clientGetItem = motor.motor_asyncio.AsyncIOMotorClient(
            f"mongodb://{Username}:{MongoDB_Password}@{Server_IP}:27017"
        )
        await init_beanie(
            database=clientGetItem.kumiko_marketplace, document_models=[Marketplace]
        )
        resMain2 = await Marketplace.find(Marketplace.name == name).to_list()
        return resMain2

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    async def edit(
        self,
        date_added: str,
        owner: int,
        name: Optional[str] = None,
        description: Optional[str] = None,
        amount: Optional[int] = None,
        price: Optional[int] = None,
    ):
        clientEditItem = motor.motor_asyncio.AsyncIOMotorClient(
            f"mongodb://{Username}:{MongoDB_Password}@{Server_IP}:27017"
        )
        await init_beanie(
            database=clientEditItem.kumiko_marketplace, document_models=[Marketplace]
        )
        entryEditItem = Marketplace(
            date_added=date_added,
            owner=owner,
            name=name,
            description=description,
            amount=amount,
            price=price,
        )
        await entryEditItem.replace()

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    async def delOneItem(self, name: str, owner: int):
        clientDelItem = motor.motor_asyncio.AsyncIOMotorClient(
            f"mongodb://{Username}:{MongoDB_Password}@{Server_IP}:27017"
        )
        await init_beanie(
            database=clientDelItem.kumiko_marketplace, document_models=[Marketplace]
        )
        entryDelItem = Marketplace.find_one(
            Marketplace.owner == owner, Marketplace.name == name
        )
        await entryDelItem.delete()

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    async def delAll(self, owner: int):
        clientDelAll = motor.motor_asyncio.AsyncIOMotorClient(
            f"mongodb://{Username}:{MongoDB_Password}@{Server_IP}:27017"
        )
        await init_beanie(
            database=clientDelAll.kumiko_marketplace, document_models=[Marketplace]
        )
        entryDelAllItem = Marketplace.find_all(Marketplace.owner == owner)
        await entryDelAllItem.delete()

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
