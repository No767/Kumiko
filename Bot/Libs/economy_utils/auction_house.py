import asyncio

import asyncio_redis
import uvloop
from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from . import models
from .db_base import Base


class KumikoAuctionHouseUtils:
    def __init__(self):
        self.self = self

    async def getItemKey(
        self, key: str, db: int, redis_server_ip: str, redis_port: int
    ):
        """Gets the keys for an item within Redis

        Args:
            key (str): The key to get
            db (int): The database to get the key from
            redis_server_ip (str): The Redis server IP
            redis_port (int): The Redis server port
        """
        conn = await asyncio_redis.Pool.create(
            host=redis_server_ip, port=int(redis_port), db=db
        )
        getKey = await conn.get(key)
        conn.close()
        return getKey

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    async def scanKeys(
        self, match: str, db: int, redis_server_ip: str, redis_port: int
    ):
        """Scans all of the values from the Redis database

        Args:
            match (str): Filter for keys by pattern
            db (int): The database to scan
            redis_server_ip (str): The Redis server IP
            redis_port (int): The Redis server port
        """
        conn = await asyncio_redis.Pool.create(
            host=redis_server_ip, port=int(redis_port), db=db
        )
        scanKeys = await conn.keys_aslist(pattern=match)
        conn.close()
        return scanKeys

    async def setItemKey(
        self,
        key: str,
        value: int,
        db: int,
        ttl: int,
        redis_server_ip: str,
        redis_port: int,
    ):
        """Sets that key within Redis

        Args:
            key (str): The key to set
            value (int): The value to set
            db (int): The database to set the key in
            ttl (int): The TTL or expire time of the key
            redis_server_ip (str): The Redis server IP
            redis_port (int): The Redis server port
        """
        conn = await asyncio_redis.Pool.create(
            host=redis_server_ip, port=int(redis_port), db=db
        )
        await conn.set(key, str(value), expire=ttl)
        conn.close()

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    async def initAHTables(self, uri: str):
        """Coroutine for creating AH tables

        Args:
            uri (str): DB Connection URI
        """
        engine = create_async_engine(
            uri,
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
        price: int,
        passed: bool,
        uri: str,
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
            uri (str): DB Connection URI
        """
        engine = create_async_engine(uri)

        async_session = sessionmaker(
            engine, expire_on_commit=False, class_=AsyncSession
        )
        async with async_session() as session:
            async with session.begin():
                auctionHouseItem = models.AuctionHouseItem(
                    uuid=uuid,
                    user_id=user_id,
                    name=name,
                    description=description,
                    date_added=date_added,
                    price=price,
                    passed=passed,
                )
                session.add_all([auctionHouseItem])
                await session.commit()

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    async def obtainUserAHItem(self, user_id: int, uri: str):
        """Obtains all of the items that a user has on the Auction House.
        These coroutines should be used sparingly, since most of the time
        it's better to pull it off from Redis instead

        Args:
            user_id (int): Discord User ID
            uri (str): DB Connection URI
        """
        engine = create_async_engine(uri)

        async_session = sessionmaker(
            engine, expire_on_commit=False, class_=AsyncSession
        )
        async with async_session() as session:
            async with session.begin():
                selectItem = select(models.AuctionHouseItem).filter(
                    models.AuctionHouseItem.user_id == user_id
                )
                res = await session.execute(selectItem)
                return [row for row in res.scalars()]

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    async def updateAHItem(self, uuid: str, price: int, uri: str):
        """Updates the price of an item on the Auction House.
        This should be used sparingly, since this will only
        commit it into the DB for persistance storage

        Args:
            uuid (str): Auction House Item UUID
            price (int): The new price of the item
            uri (str): DB Connection URI
        """
        engine = create_async_engine(uri)

        async_session = sessionmaker(
            engine, expire_on_commit=False, class_=AsyncSession
        )
        async with async_session() as session:
            async with session.begin():
                updateItem = update(
                    models.AuctionHouseItem,
                    values={models.AuctionHouseItem.price: price},
                ).filter(models.AuctionHouseItem.uuid == uuid)
                await session.execute(updateItem)
                await session.commit()

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    async def deleteAHItem(self, uuid: str, uri: str):
        """Deletes an AH item. This should only be used
        after the time limit is up. This will purge the item
        out of the database

        Args:
            uuid (str): Auction House Item UUID
            uri (str): DB Connection URI
        """
        engine = create_async_engine(uri)

        async_session = sessionmaker(
            engine, expire_on_commit=False, class_=AsyncSession
        )
        async with async_session() as session:
            async with session.begin():
                delItem = delete(models.AuctionHouseItem).filter(
                    models.AuctionHouseItem.uuid == uuid
                )
                await session.execute(delItem)
                await session.commit()

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    async def selectAHItemUUID(self, name: str, uri: str):
        """This only selects from the UUID Column and is used to grab the UUID of an item

        Args:
            name (str): The name of the AH Item
            uri (str): DB Connection URI
        """
        engine = create_async_engine(uri)

        async_session = sessionmaker(
            engine, expire_on_commit=False, class_=AsyncSession
        )
        async with async_session() as session:
            async with session.begin():
                selectItem = select(models.AuctionHouseItem.uuid).filter(
                    models.AuctionHouseItem.name == name
                )
                res = await session.execute(selectItem)
                return [row for row in res.scalars()]

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    async def selectAHItemPrice(self, uuid: str, uri: str):
        """Just grabs the price of the AH Item given

        Args:
            uuid (str): AH Item UUID
            uri (str): DB Connection URI
        """
        engine = create_async_engine(uri)

        async_session = sessionmaker(
            engine, expire_on_commit=False, class_=AsyncSession
        )
        async with async_session() as session:
            async with session.begin():
                selectItem = select(models.AuctionHouseItem.price).filter(
                    models.AuctionHouseItem.uuid == uuid
                )
                res = await session.execute(selectItem)
                return [row for row in res.scalars()]

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    async def obtainItemUUIDAuth(self, user_id: int, uri: str):
        """Obtains the UUID of an AH Item for auth purposes

        Args:
            uri (str): DB Connection URI
        """
        engine = create_async_engine(uri)

        async_session = sessionmaker(
            engine, expire_on_commit=False, class_=AsyncSession
        )
        async with async_session() as session:
            async with session.begin():
                selectItem = select(models.AuctionHouseItem.uuid).filter(
                    models.AuctionHouseItem.user_id == user_id
                )
                res = await session.execute(selectItem)
                return [row for row in res.scalars()]

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    async def obtainAHItemPassed(self, passed: bool, uri: str):
        """Obtains the date from each item. This is needed after to purge
        the item once it has expired.

        Args:
            passed (bool): Whether or not the item has passed the time limit
            uri (str): DB Connection URI
        """
        engine = create_async_engine(uri)

        async_session = sessionmaker(
            engine, expire_on_commit=False, class_=AsyncSession
        )
        async with async_session() as session:
            async with session.begin():
                selItem = select(models.AuctionHouseItem).filter(
                    models.AuctionHouseItem.passed == passed
                )
                res = await session.execute(selItem)
                return [row for row in res.scalars()]

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    async def setAHItemBoolean(self, uuid: str, passed: bool, uri: str):
        """Sets the passed col to a boolean value. This means that the
        item probably has passed it's listing date. The item is not
        purged from the db.

        Args:
            uuid (str): Auction House Item UUID
            passed (bool): Whether to set it to be passed or not
            uri (str): DB Connection URI
        """
        engine = create_async_engine(uri)

        async_session = sessionmaker(
            engine, expire_on_commit=False, class_=AsyncSession
        )
        async with async_session() as session:
            async with session.begin():
                updateItem = update(
                    models.AuctionHouseItem,
                    values={models.AuctionHouseItem.passed: passed},
                ).filter(models.AuctionHouseItem.uuid == uuid)
                await session.execute(updateItem)
                await session.commit()

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    async def selectItemNotPassed(self, passed: bool, uri: str):
        """Selects all items that have not passed the time limit. This is really
        only used to be able to show to the users the items that are active.

        Args:
            passed (bool): Whether or not the item has passed the time limit
            uri (str): DB Connection URI
        """
        engine = create_async_engine(uri)

        async_session = sessionmaker(
            engine, expire_on_commit=False, class_=AsyncSession
        )
        async with async_session() as session:
            async with session.begin():
                selItem = select(models.AuctionHouseItem).filter(
                    models.AuctionHouseItem.passed == passed
                )
                res = await session.execute(selItem)
                return [row for row in res.scalars()]

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    async def deleteUserAHItem(self, user_id: int, uuid: str, uri: str):
        """Purges one item from the DB for the user

        Args:
            user_id (int): Discord User ID
            uuid (str): AH Item UUID
            uri (str): DB Connection URI
        """

        engine = create_async_engine(uri)

        async_session = sessionmaker(
            engine, expire_on_commit=False, class_=AsyncSession
        )
        async with async_session() as session:
            async with session.begin():
                selectOneDelete = (
                    select(models.AuctionHouseItem)
                    .filter(models.AuctionHouseItem.user_id == user_id)
                    .filter(models.AuctionHouseItem.uuid == uuid)
                )
                itemSelected = await session.scalars(selectOneDelete)
                itemSelectedOne = itemSelected.one()
                await session.delete(itemSelectedOne)
                await session.commit()

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    async def purgeUserAHItems(self, user_id: int, uri: str):
        """Purges ALL of the user's items listed on the Auction House.

        Args:
            user_id (int): Discord User ID
            uri (str): DB Connection URI
        """
        engine = create_async_engine(uri)

        async_session = sessionmaker(
            engine, expire_on_commit=False, class_=AsyncSession
        )
        async with async_session() as session:
            async with session.begin():
                selAllDel = delete(models.AuctionHouseItem).filter(
                    models.AuctionHouseItem.user_id == user_id
                )
                await session.execute(selAllDel)
                await session.commit()

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    async def selectUserItemViaName(self, user_id: int, name: str, uri: str):
        """Obtains an item via the name belonging to the user

        Args:
            user_id (int): Discord User ID
            name (str): Name of the item
            uri (str): DB Connection URI
        """
        engine = create_async_engine(uri)

        async_session = sessionmaker(
            engine, expire_on_commit=False, class_=AsyncSession
        )
        async with async_session() as session:
            async with session.begin():
                selectItem = (
                    select(models.AuctionHouseItem)
                    .filter(models.AuctionHouseItem.name == name)
                    .filter(models.AuctionHouseItem.user_id == user_id)
                )
                res = await session.execute(selectItem)
                return [row for row in res.scalars()]

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    async def selectUserItemNameFirst(self, user_id: int, name: str, uri: str):
        """Selects the item via the name and just returns the first one found

        Args:
            user_id (int): Discord User ID
            name (str): Item Name
            uri (str): Connection URI
        """
        engine = create_async_engine(uri)

        async_session = sessionmaker(
            engine, expire_on_commit=False, class_=AsyncSession
        )
        async with async_session() as session:
            async with session.begin():
                selectItem = (
                    select(models.AuctionHouseItem)
                    .filter(models.AuctionHouseItem.name == name)
                    .filter(models.AuctionHouseItem.user_id == user_id)
                )
                res = await session.scalars(selectItem)
                return res.first()

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    async def selectFirstItem(self, name: str, uri: str):
        """Gets and selects the first item from the given name

        Args:
            name (str): AH Item Name
            uri (str): Connection URI
        """
        engine = create_async_engine(uri)

        async_session = sessionmaker(
            engine, expire_on_commit=False, class_=AsyncSession
        )
        async with async_session() as session:
            async with session.begin():
                selectItem = select(models.AuctionHouseItem).filter(
                    models.AuctionHouseItem.name == name
                )
                res = await session.scalars(selectItem)
                return res.first()

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    async def selectFirstItemViaUUID(self, uuid: str, uri: str):
        """Gets and selects the first item from the given UUID

        Args:
            uuid (str): AH Item UUID
            uri (str): Connection URI
        """
        engine = create_async_engine(uri)

        async_session = sessionmaker(
            engine, expire_on_commit=False, class_=AsyncSession
        )
        async with async_session() as session:
            async with session.begin():
                selectItem = select(models.AuctionHouseItem).filter(
                    models.AuctionHouseItem.uuid == uuid
                )
                res = await session.scalars(selectItem)
                return res.first()

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    async def selectAllItemsUUID(self, uri: str):
        """Selects all of the UUID's on the DB

        Args:
            uri (str): DB Connection URI
        """
        engine = create_async_engine(uri)

        async_session = sessionmaker(
            engine, expire_on_commit=False, class_=AsyncSession
        )
        async with async_session() as session:
            async with session.begin():
                selItem = select(models.AuctionHouseItem.uuid)
                res = await session.execute(selItem)
                return [row for row in res.scalars()]

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
