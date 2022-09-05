import asyncio

import uvloop
from sqlalchemy import (BigInteger, Column, Integer, String, Text, select,
                        update)
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()


class UserInv(Base):
    __tablename__ = "user_inv"

    user_uuid = Column(String, primary_key=True)
    user_id = Column(
        BigInteger,
    )
    date_acquired = Column(String)
    uuid = Column(String)
    name = Column(String)
    description = Column(Text)
    amount = Column(Integer)

    def __iter__(self):
        yield "user_uuid", self.user_uuid
        yield "user_id", self.user_id
        yield "date_acquired", self.date_acquired
        yield "uuid", self.uuid
        yield "name", self.name
        yield "description", self.description
        yield "amount", self.amount

    def __repr__(self):
        return f"UserInv(user_uuid={self.user_uuid!r}, user_id={self.user_id!r}, date_acquired={self.date_acquired!r}, uuid={self.uuid!r}, name={self.name!r}, description={self.description!r}, amount={self.amount!r})"


class KumikoUserInvUtils:
    def __init__(self):
        self.self = self

    async def initUserInvTables(self, uri: str) -> None:
        """_summary_

        Args:
            uri (str): Connection URI
        """
        engine = create_async_engine(uri, echo=True)
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
                insertUserInv = UserInv(
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
                    update(UserInv, values={UserInv.amount: amount})
                    .filter(UserInv.uuid == uuid)
                    .filter(UserInv.user_id == user_id)
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
                selectUser = select(UserInv).filter(UserInv.user_id == user_id)
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
                selectUser = select(UserInv).filter(UserInv.user_id == user_id)
                res = await session.execute(selectUser)
                return [row for row in res.scalars()]

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
