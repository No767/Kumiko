import asyncio

import uvloop
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from . import models
from .db_base import Base


class KumikoUserInvUtils:
    def __init__(self):
        self.self = self

    async def initUserInvTables(self, uri: str) -> None:
        """_summary_

        Args:
            uri (str): Connection URI
        """
        engine = create_async_engine(uri)
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    async def insertItem(
        self,
        user_uuid: str,
        user_id: int,
        date_acquired: str,
        uuid: str,
        name: str,
        description: str,
        amount: int,
        uri: str,
    ) -> None:
        """Adds the item into the user's inventory

        Args:
            user_uuid (str): User UUID
            user_id (int): Discord User ID
            date_acquired (str / ISO-8601): Date the item was acquired on or first acquired on
            uuid (str): Item UUID
            name (str): Item Name
            description (str): Item Description
            amount (int): Amount of items in the inv
            uri (str): Connection URI
        """
        engine = create_async_engine(uri)
        async_session = sessionmaker(
            engine, expire_on_commit=False, class_=AsyncSession
        )
        async with async_session() as session:
            async with session.begin():
                insertUserInv = models.UserInv(
                    user_uuid=user_uuid,
                    user_id=user_id,
                    date_acquired=date_acquired,
                    uuid=uuid,
                    name=name,
                    description=description,
                    amount=amount,
                )
                session.add_all([insertUserInv])
                await session.commit()

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    async def updateItemAmount(
        self, user_id: int, uuid: int, amount: int, uri: str
    ) -> None:
        """Updates the user to the new amount of items in the inv

        Args:
            user_id (int): Discord User ID
            uuid (str): Item UUID
            amount (int): New amount of items
            uri (str): Connection URI
        """
        engine = create_async_engine(uri)
        async_session = sessionmaker(
            engine, expire_on_commit=False, class_=AsyncSession
        )
        async with async_session() as session:
            async with session.begin():
                updateItem = (
                    update(models.UserInv, values={models.UserInv.amount: amount})
                    .filter(models.UserInv.uuid == uuid)
                    .filter(models.UserInv.user_id == user_id)
                )
                await session.execute(updateItem)
                await session.commit()

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    async def checkIfItemInUserInv(self, user_id: int, uuid: str, uri: str) -> list:
        """Checks if the item is already in the user's inv

        Args:
            user_id (int): Discord User ID
            uuid (str): Item UUID
            uri (str): Connection URI

        Returns:
            list: A list of results
        """
        engine = create_async_engine(uri)
        async_session = sessionmaker(
            engine, expire_on_commit=False, class_=AsyncSession
        )
        async with async_session() as session:
            async with session.begin():
                selectUser = select(models.UserInv).filter(
                    models.UserInv.user_id == user_id
                )
                selectUserRes = await session.execute(selectUser)
                return [
                    row for row in selectUserRes.scalars() if dict(row)["uuid"] == uuid
                ]

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    async def getUserInv(self, user_id: int, uri: str) -> list:
        """Get's the user's inv

        Args:
            user_id (int): Discord User ID
            uri (str): Connection URI

        Returns:
            list: List of Results
        """
        engine = create_async_engine(uri)
        async_session = sessionmaker(
            engine, expire_on_commit=False, class_=AsyncSession
        )
        async with async_session() as session:
            async with session.begin():
                selectUser = select(models.UserInv).filter(
                    models.UserInv.user_id == user_id
                )
                res = await session.execute(selectUser)
                return [row for row in res.scalars()]

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
