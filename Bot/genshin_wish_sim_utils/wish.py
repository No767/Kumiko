import asyncio
import os

import uvloop
from dotenv import load_dotenv
from sqlalchemy import (BigInteger, Boolean, Column, Integer, String, Text,
                        select)
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker

load_dotenv()

POSTGRES_PASSWORD = os.getenv("Postgres_Password_Dev")
POSTGRES_SERVER_IP = os.getenv("Postgres_Server_IP_Dev")
POSTGRES_DATABASE = os.getenv("Postgres_Wish_Sim_Database")
POSTGRES_USERNAME = os.getenv("Postgres_Username_Dev")
POSTGRES_PORT = os.getenv("Postgres_Port_Dev")

Base = declarative_base()
WanderlustBase = declarative_base()
UserItemBase = declarative_base()
BeginnersBase = declarative_base()


class WanderlustWSItems(WanderlustBase):

    __tablename__ = "wanderlust_wish_sim_items"
    uuid = Column(String, primary_key=True)
    name = Column(String)
    description = Column(Text)
    star_rank = Column(Integer)
    item_type = Column(String)
    event_name = Column(String)

    def __repr__(self):
        return f"WanderlustWSItems(uuid={self.uuid}, name={self.name}, description={self.description}, star_rank={self.star_rank}, item_type={self.item_type}, event_name={self.event_name})"


class BeginnersWSItems(BeginnersBase):

    __tablename__ = "beginners_wish_sim_items"
    uuid = Column(String, primary_key=True)
    name = Column(String)
    description = Column(Text)
    star_rank = Column(Integer)
    item_type = Column(String)
    event_name = Column(String)

    def __repr__(self):
        return f"BeginnersWSItems(uuid={self.uuid}, name={self.name}, description={self.description}, star_rank={self.star_rank}, item_type={self.item_type}, event_name={self.event_name})"


class UserWS(UserItemBase):

    __tablename__ = "user_ws"
    user_id = Column(BigInteger, primary_key=True)
    pulls = Column(BigInteger)
    is_active = Column(Boolean)


class UserWishSimInv(Base):

    __tablename__ = "user_wish_sim_inv"
    item_uuid = Column(String, primary_key=True)
    user_id = Column(BigInteger)
    name = Column(String)
    date_acquired = Column(String)
    star_rank = Column(Integer)
    item_type = Column(String)


class KumikoWSUtils:
    def __init__(self):
        self.self = self

    async def initAllWSTables(self):
        """Creates all of the tables"""
        engine = create_async_engine(
            f"postgresql+asyncpg://{POSTGRES_USERNAME}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER_IP}:5432/{POSTGRES_DATABASE}",
            echo=True,
        )
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
            await conn.run_sync(WanderlustBase.metadata.create_all)
            await conn.run_sync(UserItemBase.metadata.create_all)
            await conn.run_sync(BeginnersBase.metadata.create_all)

    async def addWanderlustItem(
        self, uuid: str, name: str, description: str, star_rank: int, item_type: str
    ):
        """Adds an item into the Wanderlust WS DB

        Args:
            uuid (str): The random UUID assigned to the item or character
            name (str): The name of the item or character
            description (str): The description of the item or character
            star_rank (int): The rank of the item. Determines the rarity of the item or character
            item_type (str): Either an weapon or character
        """
        engine = create_async_engine(
            f"postgresql+asyncpg://{POSTGRES_USERNAME}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER_IP}:5432/{POSTGRES_DATABASE}",
        )
        async_session = sessionmaker(
            engine, expire_on_commit=False, class_=AsyncSession
        )
        async with async_session() as session:
            async with session.begin():
                wanderlustItem = WanderlustWSItems(
                    uuid=uuid,
                    name=name,
                    description=description,
                    star_rank=star_rank,
                    item_type=item_type,
                    event_name="wanderlust",
                )
                session.add_all([wanderlustItem])
                await session.commit()

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    async def addBeginnersItem(
        self, uuid: str, name: str, description: str, star_rank: int, item_type: str
    ):
        """Adds an item into the Beginners WS DB

        Args:
            uuid (str): The random UUID assigned to the item or character
            name (str): The name of the item or character
            description (str): The description of the item or character
            star_rank (int): The rank of the item. Determines the rarity of the item or character
            item_type (str): Either an weapon or character
        """
        engine = create_async_engine(
            f"postgresql+asyncpg://{POSTGRES_USERNAME}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER_IP}:5432/{POSTGRES_DATABASE}",
        )
        async_session = sessionmaker(
            engine, expire_on_commit=False, class_=AsyncSession
        )
        async with async_session() as session:
            async with session.begin():
                beginnersItem = BeginnersWSItems(
                    uuid=uuid,
                    name=name,
                    description=description,
                    star_rank=star_rank,
                    item_type=item_type,
                    event_name="beginners",
                )
                session.add_all([beginnersItem])
                await session.commit()

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    async def getWanderlustItems(self):
        """Returns a list of all of the items in the Wanderlust WS DB"""
        engine = create_async_engine(
            f"postgresql+asyncpg://{POSTGRES_USERNAME}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER_IP}:5432/{POSTGRES_DATABASE}",
        )
        async_session = sessionmaker(
            engine, expire_on_commit=False, class_=AsyncSession
        )
        async with async_session() as session:
            async with session.begin():
                selectItem = select(WanderlustWSItems)
                res = await session.execute(selectItem)
                return [row for row in res.scalars()]

    async def getBeginnersItems(self):
        """Returns a list of all of the items in the Beginners WS DB"""
        engine = create_async_engine(
            f"postgresql+asyncpg://{POSTGRES_USERNAME}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER_IP}:5432/{POSTGRES_DATABASE}",
        )
        async_session = sessionmaker(
            engine, expire_on_commit=False, class_=AsyncSession
        )
        async with async_session() as session:
            async with session.begin():
                selectItem = select(BeginnersWSItems)
                res = await session.execute(selectItem)
                return [row for row in res.scalars()]

    async def getUserWS(self, user_id: int):
        """Get's the user's profile

        Args:
            user_id (int): Discord User ID
        """
        engine = create_async_engine(
            f"postgresql+asyncpg://{POSTGRES_USERNAME}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER_IP}:5432/{POSTGRES_DATABASE}",
        )
        async_session = sessionmaker(
            engine, expire_on_commit=False, class_=AsyncSession
        )
        async with async_session() as session:
            async with session.begin():
                selectItem = select(UserWS).filter(UserWS.user_id == user_id)
                res = await session.execute(selectItem)
                return [row for row in res.scalars()]

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
