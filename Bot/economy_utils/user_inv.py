import asyncio
import os
from typing import Optional

import motor.motor_asyncio
import uvloop
from beanie import Document, init_beanie
from dotenv import load_dotenv
from pydantic import BaseModel
from sqlalchemy import BigInteger, Column, MetaData, Table
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.asyncio import create_async_engine

load_dotenv()
MongoDB_Password = os.getenv("MongoDB_Password_Dev")
Username = os.getenv("MongoDB_Username_Dev")
Server_IP = os.getenv("MongoDB_Server_IP_Dev")

POSTGRES_PASSWORD = os.getenv("Postgres_Password_Dev")
POSTGRES_SERVER_IP = os.getenv("Postgres_Server_IP_Dev")
POSTGRES_USERNAME = os.getenv("Postgres_Username_Dev")
POSTGRES_DATABASE = os.getenv("Postgres_Database_Dev")


class Item(BaseModel):
    name: str
    description: Optional[str] = None
    amount: int
    uuid: str


class User_Inventory(Document):
    user_id: int
    item: Item


class UsersInv:
    def __init__(self):
        self.self = self

    async def insItem(self, user_id: int, item: dict):
        client = motor.motor_asyncio.AsyncIOMotorClient(
            f"mongodb://{Username}:{MongoDB_Password}@{Server_IP}:27017"
        )
        await init_beanie(
            database=client.kumiko_user_inv, document_models=[User_Inventory]
        )
        entry = User_Inventory(user_id=user_id, item=item)
        await entry.create()

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    async def obtainInv(self, discord_user_id: int):
        clientObtainInv = motor.motor_asyncio.AsyncIOMotorClient(
            f"mongodb://{Username}:{MongoDB_Password}@{Server_IP}:27017"
        )
        await init_beanie(
            database=clientObtainInv.kumiko_user_inv,
            document_models=[User_Inventory],
        )
        results = await User_Inventory.find_many(
            User_Inventory.user_id == discord_user_id
        ).to_list()
        return results

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

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
