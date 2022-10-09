import asyncio

import uvloop
from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from . import models
from .db_base import Base


class KumikoEcoUserUtils:
    def __init__(self):
        self.self = self

    async def initUserTables(self, uri: str):
        """Creates the tables needed for each user

        Args:
            uri (str): Connection URI
        """
        engine = create_async_engine(
            uri,
        )
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    async def initUserAcct(self, user_id: int, date_joined: str, uri: str):
        """Initializes a user's account

        Args:
            user_id (int): _description_
            date_joined (str): The date that the user has joined
            uri (str): The Connection URI needed for connecting to the database
        """
        engine = create_async_engine(uri)

        async_session = sessionmaker(
            engine, expire_on_commit=False, class_=AsyncSession
        )
        async with async_session() as session:
            async with session.begin():
                insertData = models.KumikoEcoUser(
                    user_id=user_id,
                    lavender_petals=0,
                    rank=0,
                    date_joined=date_joined,
                )
                session.add_all([insertData])
                await session.commit()

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    async def insertUserData(
        self, user_id: int, lavender_petals: int, rank: int, date_joined: str, uri: str
    ):
        """Inserts user data into the db

        Args:
            user_id (int): Discord User ID
            lavender_petals (int): The amount of Lavender Petals that the user has
            rank (int): The rank of the user
            date_joined (str / ISO-8601): The date that the user joined
            uri (str): The Connection URI needed for connecting to the database
        """
        engine = create_async_engine(uri)
        async_session = sessionmaker(
            engine, expire_on_commit=False, class_=AsyncSession
        )
        async with async_session() as session:
            async with session.begin():
                insertData = models.KumikoEcoUser(
                    user_id=user_id,
                    lavender_petals=lavender_petals,
                    rank=rank,
                    date_joined=date_joined,
                )
                session.add_all([insertData])
                await session.commit()

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    async def obtainUserData(self, user_id: int, uri: str):
        """Gets the data about a user

        Args:
            user_id (int): Discord User ID
            uri (str): Connection URI
        """
        engine = create_async_engine(uri)
        async_session = sessionmaker(
            engine, expire_on_commit=False, class_=AsyncSession
        )
        async with async_session() as session:
            async with session.begin():
                selectUser = select(models.KumikoEcoUser).filter(
                    models.KumikoEcoUser.user_id == user_id
                )
                res = await session.execute(selectUser)
                return [row for row in res.scalars()]

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    async def getFirstUser(self, user_id: int, uri: str):
        """Gets the first user requested

        Args:
            user_id (int): Discord User ID
            uri (str): Connection URI
        """
        engine = create_async_engine(uri)
        async_session = sessionmaker(
            engine, expire_on_commit=False, class_=AsyncSession
        )
        async with async_session() as session:
            async with session.begin():
                selectUser = select(models.KumikoEcoUser).filter(
                    models.KumikoEcoUser.user_id == user_id
                )
                itemSelected = await session.scalars(selectUser)
                itemSelectedFirst = itemSelected.first()
                return itemSelectedFirst

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    async def selectUserRank(self, user_id: int, uri: str):
        """Obtains the rank of the user

        Args:
            user_id (int): Discord User ID
            uri (str): Connection URI
        """
        engine = create_async_engine(uri)
        async_session = sessionmaker(
            engine, expire_on_commit=False, class_=AsyncSession
        )
        async with async_session() as session:
            async with session.begin():
                selectUser = select(models.KumikoEcoUser.rank).filter(
                    models.KumikoEcoUser.user_id == user_id
                )
                res = await session.execute(selectUser)
                return [row for row in res.scalars()]

    async def updateUserRank(self, user_id: int, rank: int, uri: str):
        """Updates a user's rank

        Args:
            user_id (int): Discord User ID
            rank (int): New Rank Level
            uri (str): Connection URI
        """
        engine = create_async_engine(uri)
        async_session = sessionmaker(
            engine, expire_on_commit=False, class_=AsyncSession
        )
        async with async_session() as session:
            async with session.begin():
                updateUser = update(
                    models.KumikoEcoUser, values={models.KumikoEcoUser.rank: rank}
                ).filter(models.KumikoEcoUser.user_id == user_id)
                await session.execute(updateUser)
                await session.commit()

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    async def updateUserLavenderPetals(
        self, user_id: int, lavender_petals: int, uri: str
    ):
        """Updates the amount of lavender petals that the user has

        Args:
            user_id (int): Discord User ID
            lavender_petals (int): New amount of Lavender Petals
            uri (str): Connection URI
        """
        engine = create_async_engine(uri)
        async_session = sessionmaker(
            engine, expire_on_commit=False, class_=AsyncSession
        )
        async with async_session() as session:
            async with session.begin():
                updateUser = update(
                    models.KumikoEcoUser,
                    values={models.KumikoEcoUser.lavender_petals: lavender_petals},
                ).filter(models.KumikoEcoUser.user_id == user_id)
                await session.execute(updateUser)
                await session.commit()

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    async def deleteUser(self, user_id: int, uri: str):
        """Deletes a user from the database

        Args:
            user_id (int): Discord User ID
            uri (str): Connection URI
        """
        engine = create_async_engine(uri)
        async_session = sessionmaker(
            engine, expire_on_commit=False, class_=AsyncSession
        )
        async with async_session() as session:
            async with session.begin():
                deleteUser = delete(models.KumikoEcoUser).filter(
                    models.KumikoEcoUser.user_id == user_id
                )
                await session.execute(deleteUser)
                await session.commit()

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
