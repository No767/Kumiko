import asyncio
import random

import numpy as np
import uvloop
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from . import models
from .models import Base


class KumikoWSUtils:
    def __init__(self):
        self.self = self

    async def initAllWSTables(self, uri: str) -> None:
        """Creates all of the tables

        Args:

            uri (str): Connection URI
        """
        engine = create_async_engine(
            uri,
            echo=True,
        )
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    async def addToWSData(
        self,
        uuid: str,
        event_name: str,
        name: str,
        description: str,
        star_rank: int,
        type: str,
        uri: str,
    ) -> None:
        """Adds an entry into the WS DB

        Args:
            uuid (str): WS Item UUID
            event_name (str): The name of the event
            name (str): Name of the item or character
            description (str): Description of the item or character
            star_rank (int): The rank of the item or character
            type (str): Character or Item?
            uri (str): Connection URI
        """
        engine = create_async_engine(uri)
        asyncSession = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
        async with asyncSession() as session:
            async with session.begin():
                insertItem = models.WSData(
                    uuid=uuid,
                    event_name=event_name,
                    name=name,
                    description=description,
                    star_rank=star_rank,
                    type=type,
                )
                session.add_all([insertItem])
                await session.commit()

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    async def selectAllWSData(self, uri: str) -> list:
        """Selects literally all of the data out of the DB.
        Only for testing purposes

        Args:
            uri (str): Connection URI

        Returns:
            list: List of results
        """
        engine = create_async_engine(uri)
        asyncSession = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
        async with asyncSession() as session:
            async with session.begin():
                selectItem = select(models.WSData)
                res = await session.execute(selectItem)
                return np.array([row for row in res.scalars()])

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    async def updateWSDataDescription(
        self, uuid: str, description: str, uri: str
    ) -> None:
        """Updates the WS Item with a different description

        Args:
            uuid (str): WS Item UUID
            description (str): New Description
            uri (str): Connection URI
        """
        engine = create_async_engine(uri)
        asyncSession = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
        async with asyncSession() as session:
            async with session.begin():
                updateItem = update(
                    models.WSData, values={models.WSData.description: description}
                ).where(models.WSData.uuid == uuid)
                await session.execute(updateItem)
                await session.commit()

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    async def getWSItemName(self, name: str, uri: str) -> list:
        """Returns an item from the WS DB based on that name

        Args:
            name (str): WS Item Name
            uri (str): Connection URI

        Returns:
            list: List of items
        """
        engine = create_async_engine(uri)
        asyncSession = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
        async with asyncSession() as session:
            async with session.begin():
                selItem = select(models.WSData).where(models.WSData.name == name)
                res = await session.execute(selItem)
                return [row for row in res.scalars()]

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    async def getRandomWS(self, uri: str) -> list:
        """Randomly picks out a row based on the WS Dataset

        Args:
            uri (str): Connection URI

        Returns:
            list: A list of results
        """
        engine = create_async_engine(uri)
        asyncSession = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
        async with asyncSession() as session:
            async with session.begin():
                selectItem = (
                    select(models.WSData)
                    .offset(random.randrange(25))  # nosec B311
                    .limit(1)
                )
                res = await session.execute(selectItem)
                return [row for row in res.scalars()]

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    async def getRandomWSArray(self, star_rank: int, uri: str) -> models.WSData:
        """Selects all of the data from the WS DB, and randomly picks out a row.
        Accelerated with numpy arrays.

        Args:
            star_rank (int): The star rank of the item
            uri (str): Connection URI

        Returns:
            models.WSData: An WSData object
        """
        engine = create_async_engine(uri)
        asyncSession = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
        async with asyncSession() as session:
            async with session.begin():
                selItem = select(models.WSData).filter(
                    models.WSData.star_rank == star_rank
                )
                res = await session.execute(selItem)
                npArray = np.array([row for row in res.scalars()])
                return np.random.choice(npArray)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    async def getRandomWSArrayLooped(
        self, amount: int, star_rank: int, uri: str
    ) -> np.array:
        """Loops over a random selection for a certain amount of times.
        Used for when there is a need to generate a certain amount of items

        Args:
            amount (int): The amount of times to loop for
            star_rank (int): The star rank of the item
            uri (str): Connection URI

        Returns:
            np.array: A numpy array of WSData objects
        """
        engine = create_async_engine(uri)
        asyncSession = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
        async with asyncSession() as session:
            async with session.begin():
                selItem = select(models.WSData).filter(
                    models.WSData.star_rank == star_rank
                )
                res = await session.execute(selItem)
                npArray = np.array([row for row in res.scalars()])
                return [np.random.choice(npArray) for _ in range(amount)]

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
