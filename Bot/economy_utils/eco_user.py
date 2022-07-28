import asyncio
import os

import uvloop
from dotenv import load_dotenv
from sqlalchemy import (BigInteger, Column, Integer, MetaData, String, Table,
                        delete, select, update)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker

load_dotenv()

POSTGRES_PASSWORD = os.getenv("Postgres_Password_Dev")
POSTGRES_SERVER_IP = os.getenv("Postgres_Server_IP_Dev")
POSTGRES_DATABASE = os.getenv("Postgres_Database_Dev")
POSTGRES_USERNAME = os.getenv("Postgres_Username_Dev")

Base = declarative_base()


class KumikoEcoUser(Base):
    __tablename__ = "users"

    user_id = Column(BigInteger, primary_key=True)
    lavender_petals = Column(Integer)
    rank = Column(Integer)
    date_joined = Column(String)

    def __iter__(self):
        yield "user_id", self.user_id
        yield "lavender_petals", self.lavender_petals
        yield "rank", self.rank
        yield "date_joined", self.date_joined

    def __repr__(self):
        return f"KumikoEcoUser(user_id={self.user_id}, lavender_petals={self.lavender_petals}, rank={self.rank}, date_joined={self.date_joined})"


class KumikoEcoUserUtils:
    def __init__(self):
        self.self = self

    async def initUserTables(self):
        """Creates the tables needed for each user"""
        engine = create_async_engine(
            f"postgresql+asyncpg://{POSTGRES_USERNAME}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER_IP}:5432/{POSTGRES_DATABASE}",
            echo=True,
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
                selItem = select(KumikoEcoUser).filter(KumikoEcoUser.user_id == user_id)
                results = await session.execute(selItem)
                resFetchedOne = results.one()
                fullResults = [row for row in resFetchedOne]
                if len(fullResults) == 0:
                    insertData = KumikoEcoUser(
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
                insertData = KumikoEcoUser(
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
                selectUser = select(KumikoEcoUser).filter(
                    KumikoEcoUser.user_id == user_id
                )
                res = await session.execute(selectUser)
                return [row for row in res.scalars()]

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
                selectUser = select(KumikoEcoUser.rank).filter(
                    KumikoEcoUser.user_id == user_id
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
                    KumikoEcoUser, values={KumikoEcoUser.rank: rank}
                ).filter(KumikoEcoUser.user_id == user_id)
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
                    KumikoEcoUser,
                    values={KumikoEcoUser.lavender_petals: lavender_petals},
                ).filter(KumikoEcoUser.user_id == user_id)
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
                deleteUser = delete(KumikoEcoUser).filter(
                    KumikoEcoUser.user_id == user_id
                )
                await session.execute(deleteUser)
                await session.commit()

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    ### ------ OLD COROUTINES ------ ###

    # All other methods on here (except for the initInvTable methods)
    # are deprecated. Will be removed soon.
    async def updateUser(self, owner_id: int, coins: int):
        """Updates the amount of coins a user has

        Args:
            owner_id (int): Discord User ID
            coins (int): The amount of coins to update to
        """
        meta = MetaData()
        engine = create_async_engine(
            f"postgresql+asyncpg://{POSTGRES_USERNAME}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER_IP}:5432/{POSTGRES_DATABASE}"
        )
        users = Table(
            "users",
            meta,
            Column("user_id", BigInteger),
            Column("coins", Integer),
        )
        async with engine.begin() as conn:
            update_values = (
                users.update().values(coins=coins).filter(users.c.user_id == owner_id)
            )
            await conn.execute(update_values)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    async def initTables(self):
        """Initializes the user data tables for the economy system. This is used for the Postgres-Init script."""
        meta4 = MetaData()
        engine4 = create_async_engine(
            f"postgresql+asyncpg://{POSTGRES_USERNAME}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER_IP}:5432/{POSTGRES_DATABASE}",
            echo=True,
        )
        Table(
            "users",
            meta4,
            Column("user_id", BigInteger),
            Column("coins", Integer),
        )
        async with engine4.begin() as conn4:
            await conn4.run_sync(meta4.create_all)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    # This is not deprecated...
    async def initInvTables(self):
        """Initializes the user inv tables for the economy system. This is used for the Postgres-Init script."""
        meta4 = MetaData()
        engine4 = create_async_engine(
            f"postgresql+asyncpg://{POSTGRES_USERNAME}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER_IP}:5432/{POSTGRES_DATABASE}",
            echo=True,
        )
        Table(
            "users_inventory",
            meta4,
            Column("user_id", BigInteger),
            Column("items", JSONB),
        )
        async with engine4.begin() as conn4:
            await conn4.run_sync(meta4.create_all)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    async def getUser(self, user_id: int):
        """Obtains the amount of coins a user has

        Args:
            user_id (int): Discord User ID
        """
        meta = MetaData()
        engine = create_async_engine(
            f"postgresql+asyncpg://{POSTGRES_USERNAME}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER_IP}:5432/{POSTGRES_DATABASE}"
        )
        users = Table(
            "users",
            meta,
            Column("user_id", BigInteger),
            Column("coins", Integer),
        )
        async with engine.connect() as conn:
            s = users.select(users.c.user_id == int(user_id))
            result_select = await conn.stream(s)
            async for row in result_select:
                return row

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    async def userTransaction(
        self, sender_id: int, receiver_id: int, sender_amount: int, receiver_amount: int
    ):
        """Performs a transaction between two users

        Args:
            sender_id (int): The sender's Discord User ID
            receiver_id (int): The receiver's Discord User ID
            sender_amount (int): The amount of coins to send
            receiver_amount (int): The amount of coins to receive
        """
        meta = MetaData()
        engineMain4 = create_async_engine(
            f"postgresql+asyncpg://{POSTGRES_USERNAME}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER_IP}:5432/{POSTGRES_DATABASE}"
        )
        users = Table(
            "users",
            meta,
            Column("user_id", BigInteger),
            Column("coins", Integer),
        )
        async with engineMain4.begin() as mainConn5:
            update_values = (
                users.update()
                .values(coins=sender_amount)
                .filter(users.c.user_id == sender_id)
            )
            update_values2 = (
                users.update()
                .values(coins=receiver_amount)
                .filter(users.c.user_id == receiver_id)
            )
            await mainConn5.execute(update_values)
            await mainConn5.execute(update_values2)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
