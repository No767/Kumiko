import asyncio

import uvloop
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from . import models


class KumikoWSUsersUtils:
    def __init__(self):
        self.self = self

    async def insertNewUser(
        self, user_id: int, username: str, pulls: int, date_joined: str, uri: str
    ) -> None:
        """Inserts a new user into the GWS User DB

        Args:
            user_id (int): Discord User ID
            username (str): Discord Username
            pulls (int): How much pulls the user just did
            date_joined (str): Date Joined
            uri (str): Connection URI
        """
        engine = create_async_engine(uri)
        asyncSession = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
        async with asyncSession() as session:
            async with session.begin():
                insertItem = models.UserWS(
                    user_id=user_id,
                    username=username,
                    pulls=pulls,
                    date_joined=date_joined,
                )
                session.add_all([insertItem])
                await session.commit()

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    async def getFirstUser(self, user_id: int, uri: str):
        """Gets the first user in the DB

        Args:
            user_id (int): Discord User ID
            uri (str): Connection URI
        """
        engine = create_async_engine(uri)
        asyncSession = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
        async with asyncSession() as session:
            async with session.begin():
                selItem = select(models.UserWS).filter(models.UserWS.user_id == user_id)
                res = await session.execute(selItem)
                return res.first()

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    async def updateUserPullCount(self, user_id: int, amount: int, uri: str) -> None:
        """Update the amount of pulls that the user has

        Args:
            user_id (int): Discord User ID
            amount (int): New Amount of Pulls to update to
            uri (str): Connection URI
        """
        engine = create_async_engine(uri)
        asyncSession = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
        async with asyncSession() as session:
            async with session.begin():
                updateItem = update(
                    models.UserWS, values={models.UserWS.pulls: amount}
                ).where(models.UserWS.user_id == user_id)
                await session.execute(updateItem)
                await session.commit()

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
