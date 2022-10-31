import asyncio
from typing import Optional

import motor.motor_asyncio
import uvloop
from beanie import init_beanie

from .marketplace_models import ItemAuthProject, MarketplaceModel, PurchaseProject


class KumikoEcoUtils:
    def __init__(self):
        self.self = self

    # Used: 1
    async def ins(
        self,
        uuid: str,
        date_added: str,
        owner: int,
        owner_name: str,
        uri: str,
        name: Optional[str] = None,
        description: Optional[str] = None,
        amount: Optional[int] = None,
        price: Optional[int] = None,
        updatedPrice: Optional[bool] = False,
    ):
        """Inserts an item into the MongoDB database

        Args:
            uuid (str): UUID of the item
            date_added (str): Dated added - defaults to the current date
            owner (int): Discord user's ID
            owner_name (str): Discord user's name
            uri (str): MongoDB Connection URI
            name (Optional[str], optional): The name of the item. Defaults to None.
            description (Optional[str], optional): The description of the item. Defaults to None.
            amount (Optional[int], optional): The amount that the user has. Defaults to None.
            price (Optional[int], optional): The price set by the user. Defaults to None.
            updatedPrice (Optional[bool], optional): Whether the price has been updated. Defaults to False.
        """
        client = motor.motor_asyncio.AsyncIOMotorClient(uri)
        await init_beanie(
            database=client.kumiko_marketplace, document_models=[MarketplaceModel]
        )
        entry = MarketplaceModel(
            name=name,
            description=description,
            amount=amount,
            price=price,
            date_added=date_added,
            owner=owner,
            owner_name=owner_name,
            uuid=uuid,
            updated_price=updatedPrice,
        )
        await entry.create()

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    # Used: 1
    async def obtain(self, uri: str):
        """Obtains all of the items from the marketplace

        Args:
            uri (str): MongoDB Connection URI

        Returns:
            List: List of all items in the database
        """
        clientObtain = motor.motor_asyncio.AsyncIOMotorClient(uri)
        await init_beanie(
            database=clientObtain.kumiko_marketplace, document_models=[MarketplaceModel]
        )
        resMain = await MarketplaceModel.find_all().to_list()
        return resMain

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    # Used: 3
    async def obtainUserItem(self, name: str, user_id: str, uri: str):
        """Obtains the user item from the database

        Args:
            name (str): The name of the item
            user_id (str): The Discord User ID
            uri (str): MongoDB Connection URI

        Returns:
            Object: The object containing the data of the item
        """
        clientObtainUserItem = motor.motor_asyncio.AsyncIOMotorClient(uri)
        await init_beanie(
            database=clientObtainUserItem.kumiko_marketplace,
            document_models=[MarketplaceModel],
        )
        resMain5 = await MarketplaceModel.find(
            MarketplaceModel.name == name, MarketplaceModel.owner == user_id
        ).first_or_none()
        return resMain5

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    # Used (old): 1
    async def beforePurchase(self, owner_id: int, item_name: str, uri: str):
        """Obtains the needed data before making the purchase of said item

        Args:
            owner_id (int): Owner's Discord ID
            item_name (str): The name of the item
            uri (str): MongoDB Connection URI

        Returns:
            List: List containing the data of the item(s) found
        """
        clientPurchase = motor.motor_asyncio.AsyncIOMotorClient(uri)
        await init_beanie(
            database=clientPurchase.kumiko_marketplace,
            document_models=[MarketplaceModel],
        )
        entryPurchaseInit = (
            await MarketplaceModel.find(
                MarketplaceModel.name == item_name, MarketplaceModel.owner == owner_id
            )
            .project(PurchaseProject)
            .limit(1)
            .to_list()
        )
        return entryPurchaseInit

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    # Used (old): 1
    async def purchaseAuth(self, uuid: str, uri: str):
        """Obtains the UUID for the item, which will authorize the transaction of the item

        Args:
            uuid (str): Marketplace Item UUID
            uri (str): MongoDB Connection URI

        Returns:
            List: List containing only the UUID of the item(s) found
        """
        clientItemAuth = motor.motor_asyncio.AsyncIOMotorClient(uri)
        await init_beanie(
            database=clientItemAuth.kumiko_marketplace,
            document_models=[MarketplaceModel],
        )
        entryItemAuth = (
            await MarketplaceModel.find(MarketplaceModel.uuid == uuid)
            .project(ItemAuthProject)
            .to_list()
        )
        return entryItemAuth

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    # Used (old): 4
    async def updateItemAmount(self, uuid: str, amount: int, uri: str):
        """Update the amount of the item given

        Args:
            uuid (str): The UUID of the item in the Marketplace
            amount (int): The amount of the item in the Marketplace
            uri (str): MongoDB Connection URI
        """
        clientUpdateItemPrice = motor.motor_asyncio.AsyncIOMotorClient(uri)
        await init_beanie(
            database=clientUpdateItemPrice.kumiko_marketplace,
            document_models=[MarketplaceModel],
        )
        await MarketplaceModel.find(MarketplaceModel.uuid == uuid).set(
            {MarketplaceModel.amount: amount}
        )

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    # Used (old): 1
    async def getAllOwnersItems(self, owner: int, uri: str) -> list:
        """Gets literally all of the items that the owner has in the marketplace

        Args:
            owner (int): Discord User ID
            uri (str): MongoDB Connection URI

        Returns:
            list: A list of all of the items that the owner has in the marketplace
        """
        getItems = motor.motor_asyncio.AsyncIOMotorClient(uri)
        await init_beanie(
            database=getItems.kumiko_marketplace,
            document_models=[MarketplaceModel],
        )
        return await MarketplaceModel.find(MarketplaceModel.owner == owner).to_list()

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    # Used (old): 1
    async def purgeOwnersItems(self, uuid: str, owner: int, uri: str):
        """Purges all of the owner's items listed on the marketplace

        Args:
            uuid (str): Marketplace Item UUID
            owner (int): Discord User ID
            uri (str): MongoDB Connection URI
        """
        purgeItems = motor.motor_asyncio.AsyncIOMotorClient(uri)
        await init_beanie(
            database=purgeItems.kumiko_marketplace, document_models=[MarketplaceModel]
        )
        await MarketplaceModel.find(
            MarketplaceModel.uuid == uuid, MarketplaceModel.owner == owner
        ).delete()

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
