import asyncio
import os

import uvloop
from dotenv import load_dotenv
from sqlalchemy import BigInteger, Column, MetaData, Table
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.asyncio import create_async_engine

load_dotenv()

POSTGRES_PASSWORD = os.getenv("Postgres_Password_Dev")
POSTGRES_SERVER_IP = os.getenv("Postgres_Server_IP_Dev")
POSTGRES_USERNAME = os.getenv("Postgres_Username_Dev")
POSTGRES_DATABASE = os.getenv("Postgres_Database_Dev")


class UsersInv:
    def __init__(self):
        self.self = self

    async def obtainUserInv(self, user_id: int):
        """Obtain's the Discord user's inv

        Args:
            user_id (int): Discord User ID
        """
        metaMain = MetaData()
        engine = create_async_engine(
            f"postgresql+asyncpg://{POSTGRES_USERNAME}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER_IP}:5432/{POSTGRES_DATABASE}"
        )
        usersInv = Table(
            "users_inventory",
            metaMain,
            Column("user_id", BigInteger),
            Column("items", JSONB),
        )
        async with engine.begin() as connMain:
            selectValues = usersInv.select(usersInv.c.user_id == user_id)
            results = await connMain.stream(selectValues)
            return [row async for row in results]

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    async def insertItem(self, user_id: int, item: dict):
        """Inserts an JSON item into PostgreSQL. Used for the users inv system

        Args:
            user_id (int): Discord User ID
            item (dict): Dict containing fields such as uuids, name, etc
        """
        meta = MetaData()
        engine = create_async_engine(
            f"postgresql+asyncpg://{POSTGRES_USERNAME}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER_IP}:5432/{POSTGRES_DATABASE}"
        )
        usersInv = Table(
            "users_inventory",
            meta,
            Column("user_id", BigInteger),
            Column("items", JSONB),
        )
        async with engine.begin() as conn:
            insert_values = usersInv.insert().values(user_id=user_id, items=item)
            await conn.execute(insert_values)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    async def checkForItemInInv(self, user_id: int, uuid: str):
        """Checks if the user already has the item within their inventory

        Args:
            user_id (int): Discord User ID
            uuid (str): The UUID of the Marketplace item
        """
        meta = MetaData()
        engine = create_async_engine(
            f"postgresql+asyncpg://{POSTGRES_USERNAME}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER_IP}:5432/{POSTGRES_DATABASE}"
        )
        usersInv = Table(
            "users_inventory",
            meta,
            Column("user_id", BigInteger),
            Column("items", JSONB),
        )
        async with engine.connect() as mainConn:
            selectValues = usersInv.select(usersInv.c.user_id == user_id)
            results = await mainConn.stream(selectValues)
            return [rows async for rows in results if rows[1]["uuid"] == uuid]

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    async def updateItem(self, user_id: int, item: dict):
        """Updates an JSON item into PostgreSQL. Used for the users inv system

        Args:
            user_id (int): Discord User ID
            item (dict): Dict containing fields such as uuids, name, etc
        """
        meta = MetaData()
        engine = create_async_engine(
            f"postgresql+asyncpg://{POSTGRES_USERNAME}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER_IP}:5432/{POSTGRES_DATABASE}"
        )
        usersInv = Table(
            "users_inventory",
            meta,
            Column("user_id", BigInteger),
            Column("items", JSONB),
        )
        async with engine.begin() as conn:
            insert_values = (
                usersInv.update()
                .values(items=item)
                .filter(usersInv.c.user_id == user_id)
            )
            await conn.execute(insert_values)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
