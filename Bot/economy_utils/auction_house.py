import asyncio
import os

import asyncio_redis
import uvloop
from dotenv import load_dotenv
from sqlalchemy import (BigInteger, Boolean, Column, String, Text, delete,
                        select, update)
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
    passed = Column(Boolean)

    def __iter__(self):
        yield "uuid", self.uuid
        yield "user_id", self.user_id
        yield "name", self.name
        yield "description", self.description
        yield "date_added", self.date_added
        yield "price", self.price
        yield "passed", self.passed

    def __repr__(self):
        return f"AuctionHouseItem(uuid={self.uuid!r}, user_id={self.user_id!r}, name={self.name!r}, description={self.description!r}, date_added={self.date_added!r}, price={self.price!r}, passed={self.passed!r})"


class KumikoAuctionHouseUtils:
    def __init__(self):
        self.self = self

    async def getItemKey(self, key: str, db: int):
        """Gets the keys for an item within Redis

        Args:
            key (str): The key to get
            db (int): The database to get the key from
        """
        conn = await asyncio_redis.Pool.create(
            host=REDIS_SERVER_IP, port=int(REDIS_SERVER_PORT), db=db
        )
        getKey = await conn.get(key)
        conn.close()
        return getKey

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    async def scanKeys(self, match: str, db: int):
        """Scans all of the values from the Redis database

        Args:
            match (str): Filter for keys by pattern
            db (int): The database to scan

        """
        conn = await asyncio_redis.Pool.create(
            host=REDIS_SERVER_IP, port=int(REDIS_SERVER_PORT), db=db
        )
        scanKeys = await conn.keys_aslist(pattern=match)
        conn.close()
        return scanKeys

    async def setItemKey(self, key: str, value: int, db: int, ttl: int):
        """Sets that key within Redis

        Args:
            key (str): The key to set
            value (int): The value to set
            db (int): The database to set the key in
            ttl (int): The TTL or expire time of the key
        """
        conn = await asyncio_redis.Pool.create(
            host=REDIS_SERVER_IP, port=int(REDIS_SERVER_PORT), db=db
        )
        await conn.set(key, str(value), expire=ttl)
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
        passed: bool,
    ):
        """Adds an item to the Auction House DB

        Args:
            uuid (str): UUID of the item
            user_id (int): Discord User ID
            name (str): Name of the item
            description (str): Description of the item
            date_added (str / ISO-8601): The date that it was added
            price (int): The base bidding price of the item
            passed (bool): Whether or not the item has been passed
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
                    passed=passed,
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

    async def selectAHItemUUID(self, name: str):
        """This only selects from the UUID Column and is used to grab the

        Args:
            name (str): The name of the AH Item
        """
        engine = create_async_engine(
            f"postgresql+asyncpg://{POSTGRES_USERNAME}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER_IP}:5432/{POSTGRES_DATABASE}"
        )

        async_session = sessionmaker(
            engine, expire_on_commit=False, class_=AsyncSession
        )
        async with async_session() as session:
            async with session.begin():
                selectItem = select(AuctionHouseItem.uuid).filter(
                    AuctionHouseItem.name == name
                )
                res = await session.execute(selectItem)
                return [row for row in res.scalars()]

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    async def selectAHItemPrice(self, uuid: str):
        """Just grabs the price of the AH Item given

        Args:
            uuid (str): AH Item UUID
        """
        engine = create_async_engine(
            f"postgresql+asyncpg://{POSTGRES_USERNAME}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER_IP}:5432/{POSTGRES_DATABASE}"
        )

        async_session = sessionmaker(
            engine, expire_on_commit=False, class_=AsyncSession
        )
        async with async_session() as session:
            async with session.begin():
                selectItem = select(AuctionHouseItem.price).filter(
                    AuctionHouseItem.uuid == uuid
                )
                res = await session.execute(selectItem)
                return [row for row in res.scalars()]

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    async def obtainItemUUIDAuth(self, user_id: int):
        """Obtains the UUID of an AH Item for auth purposes

        Args:
            uuid (str): AH Item UUID
        """
        engine = create_async_engine(
            f"postgresql+asyncpg://{POSTGRES_USERNAME}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER_IP}:5432/{POSTGRES_DATABASE}"
        )

        async_session = sessionmaker(
            engine, expire_on_commit=False, class_=AsyncSession
        )
        async with async_session() as session:
            async with session.begin():
                selectItem = select(AuctionHouseItem.uuid).filter(
                    AuctionHouseItem.user_id == user_id
                )
                res = await session.execute(selectItem)
                return [row for row in res.scalars()]

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    async def obtainAHItemPassed(self, passed: bool):
        """Obtains the date from each item. This is needed after to purge
        the item once it has expired.

        Args:
            passed (bool): Whether or not the item has passed the time limit
        """
        engine = create_async_engine(
            f"postgresql+asyncpg://{POSTGRES_USERNAME}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER_IP}:5432/{POSTGRES_DATABASE}"
        )

        async_session = sessionmaker(
            engine, expire_on_commit=False, class_=AsyncSession
        )
        async with async_session() as session:
            async with session.begin():
                selItem = select(AuctionHouseItem).filter(
                    AuctionHouseItem.passed == passed
                )
                res = await session.execute(selItem)
                return [row for row in res.scalars()]

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    async def setAHItemBoolean(self, uuid: str, passed: bool):
        """Sets the passed col to a boolean value. This means that the
        item probably has passed it's listing date. The item is not
        purged from the db.

        Args:
            uuid (str): Auction House Item UUID
            passed (bool): Whether to set it to be passed or not
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
                    AuctionHouseItem, values={AuctionHouseItem.passed: passed}
                ).filter(AuctionHouseItem.uuid == uuid)
                await session.execute(updateItem)
                await session.commit()

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    async def selectItemNotPassed(self, passed: bool):
        """Selects all items that have not passed the time limit. This is really
        only used to be able to show to the users the items that are active.

        Args:
            passed (bool): Whether or not the item has passed the time limit
        """
        engine = create_async_engine(
            f"postgresql+asyncpg://{POSTGRES_USERNAME}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER_IP}:5432/{POSTGRES_DATABASE}"
        )

        async_session = sessionmaker(
            engine, expire_on_commit=False, class_=AsyncSession
        )
        async with async_session() as session:
            async with session.begin():
                selItem = select(AuctionHouseItem).filter(
                    AuctionHouseItem.passed == passed
                )
                res = await session.execute(selItem)
                return [row for row in res.scalars()]

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    async def deleteUserAHItem(self, user_id: int, uuid: str):
        """Purges one item from the DB for the user

        Args:
            user_id (int): Discord User ID
            uuid (str): AH Item UUID
        """

        engine = create_async_engine(
            f"postgresql+asyncpg://{POSTGRES_USERNAME}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER_IP}:5432/{POSTGRES_DATABASE}"
        )

        async_session = sessionmaker(
            engine, expire_on_commit=False, class_=AsyncSession
        )
        async with async_session() as session:
            async with session.begin():
                selectOneDelete = (
                    select(AuctionHouseItem)
                    .filter(AuctionHouseItem.user_id == user_id)
                    .filter(AuctionHouseItem.uuid == uuid)
                )
                itemSelected = await session.scalars(selectOneDelete)
                itemSelectedOne = itemSelected.one()
                await session.delete(itemSelectedOne)
                await session.commit()

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    async def purgeUserAHItems(self, user_id: int):
        """Purges ALL of the user's items listed on the Auction House.

        Args:
            user_id (int): Discord User ID
        """
        engine = create_async_engine(
            f"postgresql+asyncpg://{POSTGRES_USERNAME}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER_IP}:5432/{POSTGRES_DATABASE}"
        )

        async_session = sessionmaker(
            engine, expire_on_commit=False, class_=AsyncSession
        )
        async with async_session() as session:
            async with session.begin():
                selAllDel = delete(AuctionHouseItem).filter(
                    AuctionHouseItem.user_id == user_id
                )
                await session.execute(selAllDel)
                await session.commit()

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    async def selectUserItemViaName(self, user_id: int, name: str):
        """Obtains an item via the name belonging to the user

        Args:
            user_id (int): Discord User ID
            name (str): Name of the item
        """
        engine = create_async_engine(
            f"postgresql+asyncpg://{POSTGRES_USERNAME}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER_IP}:5432/{POSTGRES_DATABASE}"
        )

        async_session = sessionmaker(
            engine, expire_on_commit=False, class_=AsyncSession
        )
        async with async_session() as session:
            async with session.begin():
                selectItem = (
                    select(AuctionHouseItem)
                    .filter(AuctionHouseItem.name == name)
                    .filter(AuctionHouseItem.user_id == user_id)
                )
                res = await session.execute(selectItem)
                return [row for row in res.scalars()]

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    async def selectAllItemsUUID(self):
        """Selects all of the UUID's on the DB"""
        engine = create_async_engine(
            f"postgresql+asyncpg://{POSTGRES_USERNAME}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER_IP}:5432/{POSTGRES_DATABASE}"
        )

        async_session = sessionmaker(
            engine, expire_on_commit=False, class_=AsyncSession
        )
        async with async_session() as session:
            async with session.begin():
                selItem = select(AuctionHouseItem.uuid)
                res = await session.execute(selItem)
                return [row for row in res.scalars()]

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
