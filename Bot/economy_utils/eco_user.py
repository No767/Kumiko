import asyncio
import os

import uvloop
from dotenv import load_dotenv
from sqlalchemy import BigInteger, Column, Integer, MetaData, Table, select
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.asyncio import create_async_engine

load_dotenv()

POSTGRES_PASSWORD = os.getenv("Postgres_Password_Dev")
POSTGRES_SERVER_IP = os.getenv("Postgres_Server_IP_Dev")
POSTGRES_DATABASE = os.getenv("Postgres_Database_Dev")
POSTGRES_USERNAME = os.getenv("Postgres_Username_Dev")


class KumikoEcoUserUtils:
    def __init__(self):
        self.self = self

    async def insUserFirstTime(self, user_id: int):
        """Initializes a user's account

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
        async with engine.begin() as conn:
            s = select(users.c.user_id).where(users.c.user_id == user_id)
            results = await conn.execute(s)
            results_fetched = results.fetchone()
            if results_fetched is None:
                insert_new = users.insert().values(coins=0, user_id=user_id)
                await conn.execute(insert_new)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

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

    async def removeUser(self, user_id: int):
        """Removes a user from the database

        Args:
            user_id (int): Discord User ID
        """
        meta = MetaData()
        engineMain2 = create_async_engine(
            f"postgresql+asyncpg://{POSTGRES_USERNAME}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER_IP}:5432/{POSTGRES_DATABASE}"
        )
        users = Table(
            "users",
            meta,
            Column("user_id", BigInteger),
            Column("coins", Integer),
        )
        async with engineMain2.begin() as mainConn2:
            delete_values = users.delete().where(users.c.user_id == user_id)
            await mainConn2.execute(delete_values)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
