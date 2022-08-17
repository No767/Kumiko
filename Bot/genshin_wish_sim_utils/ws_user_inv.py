import asyncio

import numpy as np
import uvloop
from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from . import models
from .ws_users import KumikoWSUsersUtils

wsUserUtils = KumikoWSUsersUtils()


class KumikoWSUserInvUtils:
    def __init__(self):
        self.self = self

    async def insertWSItemToUserInv(
        self,
        uuid: str,
        user_id: int,
        date_obtained: str,
        name: str,
        description: str,
        star_rank: int,
        type: str,
        amount: int,
        uri: str,
    ) -> None:
        """Inserts an item into the WS user inv

        Args:
            uuid (str): WS Item UUID
            user_id (int): Discord User ID
            date_obtained (str / ISO-8601): Date the item was obtained
            name (str): Name of the item
            description (str): Description of the item
            star_rank (int): Star Rank of the item
            type (str): The type of the item
            amount (int): The amount of the item
            uri (str): Connection URI
        """
        engine = create_async_engine(uri)
        asyncSession = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
        async with asyncSession() as session:
            async with session.begin():
                checkUserProfile = await wsUserUtils.getUserProfile(
                    user_id=user_id, uri=uri
                )
                insertItemMain = models.UserWSInv(
                    item_uuid=uuid,
                    user_id=user_id,
                    date_obtained=date_obtained,
                    name=name,
                    description=description,
                    star_rank=star_rank,
                    type=type,
                    amount=amount,
                )
                session.add_all([insertItemMain])
                await session.commit()
                if len(checkUserProfile) == 0:
                    await wsUserUtils.insertNewUser(
                        user_id=user_id, pulls=1, date_joined=date_obtained, uri=uri
                    )

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    async def getUserInv(self, user_id: int, uri: str) -> np.array:
        """Gets the user's inv for Kumiko's GWS

        Args:
            user_id (int): Discord User ID
            uri (str): Connection URI

        Returns:
            np.array: A numpy array of UserWSInv objects
        """
        engine = create_async_engine(uri)
        asyncSession = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
        async with asyncSession() as session:
            async with session.begin():
                selectUserInv = select(models.UserWSInv).where(
                    models.UserWSInv.user_id == user_id
                )
                res = await session.execute(selectUserInv)
                return np.array([row for row in res.scalars()])

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    async def deleteOneUserInv(self, user_id: int, uuid: str, uri: str) -> None:
        """Deletes one item from the user's inv

        Args:
            user_id (int): Discord User ID
            uuid (str): GWS Item UUID
            uri (str): Connection URI
        """
        engine = create_async_engine(uri)
        asyncSession = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
        async with asyncSession() as session:
            async with session.begin():
                selectOneDelete = (
                    select(models.UserWSInv)
                    .filter(models.UserWSInv.user_id == user_id)
                    .filter(models.UserWSInv.item_uuid == uuid)
                )
                itemSelected = await session.scalars(selectOneDelete)
                itemSelectedFirst = itemSelected.one()
                await session.delete(itemSelectedFirst)
                await session.commit()

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    async def purgeUserInv(self, user_id: int, uri: str) -> None:
        """Purges all of the items in that user's inv. Use sparsely

        Args:
            user_id (int): Discord User ID
            uri (str): Connection URI
        """
        engine = create_async_engine(uri)
        asyncSession = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
        async with asyncSession() as session:
            async with session.begin():
                selectUserDelete = delete(models.UserWSInv).where(
                    models.UserWSInv.user_id == user_id
                )
                await session.execute(selectUserDelete)
                await session.commit()

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    async def getWSItemUserInvOne(
        self, user_id: int, name: str, uri: str
    ) -> models.UserWSInv:
        """Gets one item from the user's inv based on that name

        Args:
            user_id (int): Discord User ID
            name (str): Name of the item
            uri (str): Connection URI

        Returns:
            models.UserWSInv: A UserWSInv object (hopefully)
        """
        engine = create_async_engine(uri)
        asyncSession = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
        async with asyncSession() as session:
            async with session.begin():
                selItem = (
                    select(models.UserWSInv)
                    .where(models.UserWSInv.user_id == user_id)
                    .where(models.UserWSInv.name == name)
                )
                itemSelected = await session.scalars(selItem)
                return [itemSelected.first()]

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    async def updateWSItemAmount(
        self, user_id: int, uuid: str, amount: int, uri: str
    ) -> None:
        """Updates the amount of an item in the user's inv

        Args:
            user_id (int): Discord User ID
            uuid (str): GWS Item UUID
            amount (int): The amount of the item
            uri (str): Connection URI
        """
        engine = create_async_engine(uri)
        asyncSession = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
        async with asyncSession() as session:
            async with session.begin():
                updateItem = (
                    update(models.UserWSInv, values={models.UserWSInv.amount: amount})
                    .filter(models.UserWSInv.item_uuid == uuid)
                    .filter(models.UserWSInv.user_id == user_id)
                )
                await session.execute(updateItem)
                await session.commit()

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
