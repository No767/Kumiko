import asyncio
import os
from typing import Optional

import motor.motor_asyncio
import uvloop
from beanie import Document, init_beanie
from dotenv import load_dotenv
from pydantic import BaseModel

from .eco_user import KumikoEcoUserUtils

load_dotenv()
MongoDB_Password = os.getenv("MongoDB_Password_Dev")
Username = os.getenv("MongoDB_Username_Dev")
Server_IP = os.getenv("MongoDB_Server_IP_Dev")
usersUtils = KumikoEcoUserUtils()


class Marketplace(Document):
    name: str
    description: Optional[str] = None
    amount: int
    price: int
    date_added: str
    owner: int
    uuid: str


class ProjectOnlyID(BaseModel):
    owner: int


class PurchaseProject(BaseModel):
    owner: int
    name: str
    description: str
    price: int
    amount: int
    uuid: str


class ItemAuthProject(BaseModel):
    uuid: str


class KumikoEcoUtils:
    def __init__(self):
        self.self = self

    async def ins(
        self,
        uuid: str,
        date_added: str,
        owner: int,
        name: Optional[str] = None,
        description: Optional[str] = None,
        amount: Optional[int] = None,
        price: Optional[int] = None,
    ):
        """Inserts an item into the MongoDB database

        Args:
            uuid (str): UUID of the item
            date_added (str): Dated added - defaults to the current date
            owner (int): Discord uesr's ID
            name (Optional[str], optional): The name of the item. Defaults to None.
            description (Optional[str], optional): The description of the item. Defaults to None.
            amount (Optional[int], optional): The amount that the user has. Defaults to None.
            price (Optional[int], optional): The price set by the user. Defaults to None.
        """
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
            uuid=uuid,
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
        """Updates an item in the MongoDB database

        Args:
            date_added (str): The Date Added
            owner (int): Discord Owner ID
            name (Optional[str], optional): The Item's Name. Defaults to None.
            description (Optional[str], optional): Item Description. Defaults to None.
            amount (Optional[int], optional): Item Amount. Defaults to None.
            price (Optional[int], optional): Item Price. Defaults to None.
        """
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
        """Obtains all Id

        Returns:
            List: List of all items in the database
        """
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

    async def beforePurchase(self, owner_id: int, item_name: str):
        clientPurchase = motor.motor_asyncio.AsyncIOMotorClient(
            f"mongodb://{Username}:{MongoDB_Password}@{Server_IP}:27017"
        )
        await init_beanie(
            database=clientPurchase.kumiko_marketplace, document_models=[Marketplace]
        )
        entryPurchaseInit = (
            await Marketplace.find(
                Marketplace.name == item_name, Marketplace.owner == owner_id
            )
            .project(PurchaseProject)
            .to_list()
        )
        return entryPurchaseInit

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    async def purchaseAuth(self, uuid: str):
        """Obtains the UUID for the item, which will authorize the transaction of the item

        Args:
            uuid (str): Marketplace Item UUID
        """
        clientItemAuth = motor.motor_asyncio.AsyncIOMotorClient(
            f"mongodb://{Username}:{MongoDB_Password}@{Server_IP}:27017"
        )
        await init_beanie(
            database=clientItemAuth.kumiko_marketplace, document_models=[Marketplace]
        )
        entryItemAuth = (
            await Marketplace.find(Marketplace.uuid == uuid)
            .project(ItemAuthProject)
            .to_list()
        )
        return entryItemAuth

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    async def delItemUUID(self, uuid: str):
        """Deletes one item from the marketplace via the UUID

        Args:
            uuid (str): Marketplace Item UUID
        """
        clientItemDelete = motor.motor_asyncio.AsyncIOMotorClient(
            f"mongodb://{Username}:{MongoDB_Password}@{Server_IP}:27017"
        )
        await init_beanie(
            database=clientItemDelete.kumiko_marketplace, document_models=[Marketplace]
        )
        entryItemDelete = Marketplace.find(Marketplace.uuid == uuid)
        await entryItemDelete.delete()

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    async def searchForID(self, uuid: str):
        clientSearchID = motor.motor_asyncio.AsyncIOMotorClient(
            f"mongodb://{Username}:{MongoDB_Password}@{Server_IP}:27017"
        )
        await init_beanie(
            database=clientSearchID.kumiko_marketplace, document_models=[Marketplace]
        )
        searchItemID = Marketplace.find(Marketplace.uuid == uuid)
        return [item async for item in searchItemID]

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    async def updateItemAmount(self, uuid: str, amount: int):
        """Update the amount of the item given

        Args:
            uuid (str): The UUID of the item in the Marketplace
            amount (int): The amount of the item in the Marketplace
        """
        clientUpdateItemPrice = motor.motor_asyncio.AsyncIOMotorClient(
            f"mongodb://{Username}:{MongoDB_Password}@{Server_IP}:27017"
        )
        await init_beanie(
            database=clientUpdateItemPrice.kumiko_marketplace,
            document_models=[Marketplace],
        )
        await Marketplace.find(Marketplace.uuid == uuid).set(
            {Marketplace.amount: amount}
        )

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
