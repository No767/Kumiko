import asyncio
import uuid
from typing import Optional, Union

import motor.motor_asyncio
import uvloop
from beanie import init_beanie
from discord.utils import utcnow
from sqlalchemy.engine.row import Row

from .marketplace_models import MarketplaceModel
from .user_inv import KumikoUserInvUtils


class KumikoEcoUtils:
    def __init__(self):
        self.self = self
        self.userInvUtils = KumikoUserInvUtils()

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

    async def getRequestedPurchaseItem(self, name: str, uri: str):
        """Gets the first or none item that matches the name

        This is used to first search up the item to purchase from the Marketplace

        Args:
            name (str): The name of the item to search up
            uri (str): MongoDB Connection URI
        """
        clientPurchase = motor.motor_asyncio.AsyncIOMotorClient(uri)
        await init_beanie(
            database=clientPurchase.kumiko_marketplace,
            document_models=[MarketplaceModel],
        )
        return await MarketplaceModel.find(
            MarketplaceModel.name == name
        ).first_or_none()

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    async def setCurrentStock(self, uuid: str, amount: int, uri: str) -> None:
        """Sets the current stock amount for the requested item (checked using the UUID provided)

        Args:
            uuid (str): Requested Item UUID
            amount (int): The amount to set to. This is also commonly used to set it to be 0
            uri (str): MongoDB Connection URI
        """
        clientUpdate = motor.motor_asyncio.AsyncIOMotorClient(uri)
        await init_beanie(
            database=clientUpdate.kumiko_marketplace,
            document_models=[MarketplaceModel],
        )
        marketplaceItem = await MarketplaceModel.find_one(MarketplaceModel.uuid == uuid)
        marketplaceItem.amount = amount
        await marketplaceItem.save()

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    async def purchaseItem(
        self,
        user_inv: Union[Row, None],
        requested_item: Union[MarketplaceModel, None],
        current_stock: int,
        requested_amount: int,
        user_id: int,
        mongo_uri: str,
        postgres_uri: str,
    ):
        """Makes the purchase for the requested item

        This should be used with purchasing the item

        Args:
            user_inv (Union[Row, None]): The object (can be None) of the user's inventory
            requested_item (Union[MarketplaceModel, None]): Object (can be None) of the requested item
            current_stock (int): The current stock that the requested item has
            requested_amount (int): The amount that is requested to be purchased for
            user_id (int): The Discord user's ID
            mongo_uri (str): MongoDB Connection URI
            postgres_uri (str): PostgreSQL Connection URI
        """
        requestedItemUUID = dict(requested_item)["uuid"]
        returnStr = ""
        if user_inv is None:
            await self.updateItemAmount(
                uuid=requestedItemUUID, amount=current_stock, uri=mongo_uri
            )
            await self.userInvUtils.insertItem(
                user_uuid=str(uuid.uuid4()),
                user_id=user_id,
                date_acquired=utcnow().isoformat(),
                name=dict(requested_item)["name"],
                description=dict(requested_item)["description"],
                amount=requested_amount,
                uri=postgres_uri,
            )
            returnStr = f"Purchased {requested_amount} {dict(requested_item)['name']} for {dict(requested_item)['price']} coins. Also added {dict(requested_item)['name']} to your inventory."
        else:
            amountAddingToUser = int(dict(user_inv[0])["amount"]) + int(
                requested_amount
            )
            await self.updateItemAmount(
                uuid=requestedItemUUID, amount=current_stock, uri=mongo_uri
            )
            await self.userInvUtils.updateItemAmount(
                user_id=user_id,
                uuid=requestedItemUUID,
                amount=amountAddingToUser,
                uri=postgres_uri,
            )
            returnStr = f"Purchased {requested_amount} {dict(requested_item)['name']} for {dict(requested_item)['price']} coins."

        return returnStr

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
