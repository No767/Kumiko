import asyncio
import os

import asyncio_redis
import uvloop
from dotenv import load_dotenv
from sqlalchemy import BigInteger, Column, String, Text, delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker

load_dotenv()
REDIS_SERVER_IP = os.getenv("Redis_Server_IP_Dev")
REDIS_SERVER_PORT = os.getenv("Redis_Port_Dev")
POSTGRES_PASSWORD = os.getenv("Postgres_Password_Dev")
POSTGRES_SERVER_IP = os.getenv("Postgres_Server_IP_Dev")
POSTGRES_USERNAME = os.getenv("Postgres_Username_Dev")
POSTGRES_DATABASE = os.getenv("Postgres_Database_AH_Dev")

Base = declarative_base()


class AuctionHouseItem(Base):
    __tablename__ = "auction_house_items"

    uuid = Column(String, primary_key=True)
    user_id = Column(BigInteger)
    name = Column(String)
    description = Column(Text)
    date_added = Column(String)
    price = Column(BigInteger)

    def __iter__(self):
        yield "uuid", self.uuid
        yield "user_id", self.user_id
        yield "name", self.name
        yield "description", self.description
        yield "date_added", self.date_added
        yield "base_price", self.price

    def __repr__(self):
        return f"AuctionHouseItem(uuid={self.uuid!r}, user_id={self.user_id!r}, name={self.name!r}, description={self.description!r}, date_added={self.date_added!r}, price={self.price!r})"


class KumikoAuctionHouseUtils:
    def __init__(self):
        self.self = self

    async def getItemKey(self, key: str):
        """Gets the keys for an item within Redis

        Args:
            key (str): The key to get
        """
        conn = await asyncio_redis.Pool.create(
            host=REDIS_SERVER_IP, port=int(REDIS_SERVER_PORT)
        )
        getKey = await conn.get(key)
        conn.close()
        return getKey

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    async def setItemKey(self, key: str, value: int):
        """Sets that key within Redis

        Args:
            key (str): The key to set
            value (int): The value to set
        """
        conn = await asyncio_redis.Pool.create(
            host=REDIS_SERVER_IP, port=int(REDIS_SERVER_PORT)
        )
        await conn.set(key, str(value))
        conn.close()

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    async def initAHTables(self):
        """Coroutine for creating AH tables"""
        engine = create_async_engine(
            f"postgresql+asyncpg://{POSTGRES_USERNAME}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER_IP}:5432/{POSTGRES_DATABASE}",
            echo=True,
        )
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    async def addAuctionHouseItem(
        self,
        uuid: str,
        user_id: int,
        name: str,
        description: str,
        date_added: str,
        base_price: int,
    ):
        """Adds an item to the Auction House DB

        Args:
            uuid (str): UUID of the item
            user_id (int): Discord User ID
            name (str): Name of the item
            description (str): Description of the item
            date_added (str / ISO-8601): The date that it was added
            price (int): The base bidding price of the item
        """
        engine = create_async_engine(
            f"postgresql+asyncpg://{POSTGRES_USERNAME}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER_IP}:5432/{POSTGRES_DATABASE}"
        )

        async_session = sessionmaker(
            engine, expire_on_commit=False, class_=AsyncSession
        )
        async with async_session() as session:
            async with session.begin():
                auctionHouseItem = AuctionHouseItem(
                    uuid=uuid,
                    user_id=user_id,
                    name=name,
                    description=description,
                    date_added=date_added,
                    price=base_price,
                )
                session.add_all([auctionHouseItem])
                await session.commit()

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    async def obtainUserAHItem(self, user_id: int):
        """Obtains all of the items that a user has on the Auction House.
        These coroutines should be used sparingly, since most of the time
        it's better to pull it off from Redis instead

        Args:
            user_id (int): Discord UserID
        """
        engine = create_async_engine(
            f"postgresql+asyncpg://{POSTGRES_USERNAME}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER_IP}:5432/{POSTGRES_DATABASE}"
        )

        async_session = sessionmaker(
            engine, expire_on_commit=False, class_=AsyncSession
        )
        async with async_session() as session:
            async with session.begin():
                selectItem = select(AuctionHouseItem).filter(
                    AuctionHouseItem.user_id == user_id
                )
                res = await session.execute(selectItem)
                return [row for row in res.scalars()]

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    async def updateAHItem(self, uuid: str, price: int):
        """Updates the price of an item on the Auction House.
        This should be used sparingly, since this will only
        commit it into the DB for persistance storage

        Args:
            uuid (str): Auction House Item UUID
            price (int): The new price of the item
        """
        engine = create_async_engine(
            f"postgresql+asyncpg://{POSTGRES_USERNAME}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER_IP}:5432/{POSTGRES_DATABASE}"
        )

        async_session = sessionmaker(
            engine, expire_on_commit=False, class_=AsyncSession
        )
        async with async_session() as session:
            async with session.begin():
                updateItem = update(
                    AuctionHouseItem, values={AuctionHouseItem.price: price}
                ).filter(AuctionHouseItem.uuid == uuid)
                await session.execute(updateItem)
                await session.commit()

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    async def deleteAHItem(self, uuid: str):
        """Deletes an AH item. This should only be used
        after the time limit is up. This will purge the item
        out of the database

        Args:
            uuid (str): Auction House Item UUID
        """
        engine = create_async_engine(
            f"postgresql+asyncpg://{POSTGRES_USERNAME}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER_IP}:5432/{POSTGRES_DATABASE}"
        )

        async_session = sessionmaker(
            engine, expire_on_commit=False, class_=AsyncSession
        )
        async with async_session() as session:
            async with session.begin():
                delItem = delete(AuctionHouseItem).filter(AuctionHouseItem.uuid == uuid)
                await session.execute(delItem)
                await session.commit()

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
