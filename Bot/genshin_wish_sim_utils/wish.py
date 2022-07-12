import asyncio
import os

import uvloop
from dotenv import load_dotenv
from sqlalchemy import BigInteger, Column, Integer, String
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker

load_dotenv()

POSTGRES_PASSWORD = os.getenv("Postgres_Password_Dev")
POSTGRES_SERVER_IP = os.getenv("Postgres_Server_IP_Dev")
POSTGRES_DATABASE = os.getenv("Postgres_Wish_Sim_Database")
POSTGRES_USERNAME = os.getenv("Postgres_Username_Dev")
POSTGRES_PORT = os.getenv("Postgres_Port_Dev")

Base = declarative_base()
ItemBase = declarative_base()


class WSItems(ItemBase):

    __tablename__ = "wish_sim_items"
    item_uuid = Column(String, primary_key=True)
    name = Column(String)
    star_rank = Column(Integer)
    item_type = Column(String)

    def __repr__(self):
        returnStructItem = f"WSItems(item_uuid='{self.item_uuid!r}', name='{self.name!r}', date_acquired='{self.date_acquired!r}', star_rank='{self.star_rank!r}', item_type='{self.item_type!r}')"
        return returnStructItem


class UserWishSimInv(Base):

    __tablename__ = "user_wish_sim_inv"
    item_uuid = Column(String, primary_key=True)
    user_id = Column(BigInteger)
    name = Column(String)
    date_acquired = Column(String)
    star_rank = Column(Integer)
    item_type = Column(String)

    def __repr__(self):
        returnStruct = f"UserWishSimInv(item_uuid={self.item_uuid!r}, user_id={self.user_id!r}, name={self.name!r}, description={self.description!r}, date_acquired={self.date_acquired!r}, star_rank={self.star_rank!r})"
        return returnStruct


class KumikoWSUtils:
    def __init__(self):
        self.self = self

    async def initWSItemTable(self):
        """Creates the tables needed with the correct schema for the WS Items"""
        engine = create_async_engine(
            f"postgresql+asyncpg://{POSTGRES_USERNAME}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER_IP}:5432/{POSTGRES_DATABASE}",
            echo=True,
        )
        async with engine.begin() as conn:
            await conn.run_sync(ItemBase.metadata.create_all)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    async def initUserWSInvTable(self):
        """Creates the tables needed with the correct schema for the user's WS Items"""
        engine = create_async_engine(
            f"postgresql+asyncpg://{POSTGRES_USERNAME}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER_IP}:5432/{POSTGRES_DATABASE}",
            echo=True,
        )
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    async def addWSItem(
        self, item_uuid: str, name: str, star_rank: int, item_type: str
    ):
        """Adds an item into the WS Items DB

        Args:
            item_uuid (str): _description_
            name (str): _description_
            star_rank (int): _description_
            item_type (str): _description_
        """
        engine = create_async_engine(
            f"postgresql+asyncpg://{POSTGRES_USERNAME}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER_IP}:5432/{POSTGRES_DATABASE}",
        )
        async_session = sessionmaker(
            engine, expire_on_commit=False, class_=AsyncSession
        )
        async with async_session() as session:
            async with session.begin():
                wishSimItem = WSItems(
                    item_uuid=item_uuid,
                    name=name,
                    star_rank=star_rank,
                    item_type=item_type,
                )
                session.add_all([wishSimItem])
                await session.commit()
