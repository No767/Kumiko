import asyncio
from typing import Union

import uvloop
from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from . import models
from .db_base import Base


class KumikoQuestsUtils:
    def __init__(self):
        self.self = self

    async def initQuestsTables(self, uri: str) -> None:
        """Initializes the tables for Kumiko's Quests system

        Args:
            uri (str): Connection URI
        """
        engine = create_async_engine(uri)
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    async def createQuests(
        self,
        uuid: str,
        creator: int,
        claimed_by: Union[None, int],
        date_created: str,
        end_datetime: str,
        name: str,
        description: str,
        reward: int,
        active: bool,
        claimed: bool,
        uri: str,
    ) -> None:
        """Inserts a new quest into the database

        Args:
            uuid (str): Quests Item UUID
            creator (int): Discord User ID of the creator
            claimed_by (Union[None, int]): Discord User ID that claims this quest
            date_created (str): The creation date of the quest
            end_datetime (str): The end date and time of the quest
            name (str): Quest Name
            description (str): Quest Description
            reward (int): Quest Reward
            active (bool): Quest Active Status
            claimed (bool): Is the quest already claimed?
            uri (str): Connection URI
        """
        engine = create_async_engine(uri)
        async_session = sessionmaker(
            engine, expire_on_commit=False, class_=AsyncSession
        )
        async with async_session() as session:
            async with session.begin():
                addItemQuests = models.KumikoQuests(
                    uuid=uuid,
                    creator=creator,
                    claimed_by=claimed_by,
                    date_created=date_created,
                    end_datetime=end_datetime,
                    name=name,
                    description=description,
                    reward=reward,
                    active=active,
                    claimed=claimed,
                )
                session.add_all([addItemQuests])
                await session.commit()

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    async def getActiveQuests(self, active: bool, uri: str) -> list:
        """Gets all active quests

        Args:
            active (bool): Quest Active Status
            uri (str): Connection URI

        Returns:
            list: List of results
        """
        engine = create_async_engine(uri)
        async_session = sessionmaker(
            engine, expire_on_commit=False, class_=AsyncSession
        )
        async with async_session() as session:
            async with session.begin():
                selectItem = select(models.KumikoQuests).filter(
                    models.KumikoQuests.active == active
                )
                res = await session.execute(selectItem)
                return [row for row in res.scalars()]

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    async def getAllQuests(self, uri: str) -> list:
        """Get all of the quests in the db. Even it is active
        or not

        Args:
            uri (str): Conenction URI

        Returns:
            list: List of results
        """
        engine = create_async_engine(uri)
        async_session = sessionmaker(
            engine, expire_on_commit=False, class_=AsyncSession
        )
        async with async_session() as session:
            async with session.begin():
                selectItem = select(models.KumikoQuests)
                res = await session.execute(selectItem)
                return [row for row in res.scalars()]

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    async def updateQuest(
        self, uuid: str, reward: int, new_end_datetime: str, uri: str
    ) -> None:
        """Updates a quest with the new date and time and

        Args:
            uuid (str): Quests Item UUID
            reward (int): Quest Reward
            new_end_datetime (str): The new date and time
            uri (str): Connection URI
        """
        engine = create_async_engine(uri)
        async_session = sessionmaker(
            engine, expire_on_commit=False, class_=AsyncSession
        )
        async with async_session() as session:
            async with session.begin():
                updateItem = update(
                    models.KumikoQuests,
                    values={
                        models.KumikoQuests.end_datetime: new_end_datetime,
                        models.KumikoQuests.reward: reward,
                    },
                ).filter(models.KumikoQuests.uuid == uuid)
                await session.execute(updateItem)
                await session.commit()

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    async def getQuestViaName(self, name: str, uri: str) -> list:
        """Gets the quest via the name

        Args:
            name (str): Quest Name
            uri (str): Connection URI

        Returns:
            list: List of results
        """
        engine = create_async_engine(uri)
        async_session = sessionmaker(
            engine, expire_on_commit=False, class_=AsyncSession
        )
        async with async_session() as session:
            async with session.begin():
                getQuest = select(models.KumikoQuests).filter(
                    models.KumikoQuests.name == name
                )
                res = await session.execute(getQuest)
                return [row for row in res.scalars()]

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    async def getUserQuestOne(self, user_id: int, name: str, uri: str) -> list:
        """Gets one quest from the user

        Args:
            user_id (int): Discord User ID
            uri (str): Connection URI

        Returns:
            list: List of results
        """
        engine = create_async_engine(uri)
        async_session = sessionmaker(
            engine, expire_on_commit=False, class_=AsyncSession
        )
        async with async_session() as session:
            async with session.begin():
                getQuest = (
                    select(models.KumikoQuests)
                    .filter(models.KumikoQuests.creator == user_id)
                    .filter(models.KumikoQuests.name == name)
                )
                getQuestSelected = await session.scalars(getQuest)
                getQuestSelectedOne = getQuestSelected.first()
                return getQuestSelectedOne

    async def deleteOneQuest(self, user_id: int, uuid: str, uri: str) -> None:
        """Deletes one quest from the DB

        Args:
            user_id (int): Discord User ID
            uuid (str): Quest UUID
            uri (str): Connection URI
        """
        engine = create_async_engine(uri)
        async_session = sessionmaker(
            engine, expire_on_commit=False, class_=AsyncSession
        )
        async with async_session() as session:
            async with session.begin():
                selectOneDelete = (
                    select(models.KumikoQuests)
                    .filter(models.KumikoQuests.uuid == uuid)
                    .filter(models.KumikoQuests.creator == user_id)
                )
                itemSelected = await session.scalars(selectOneDelete)
                itemSelectedOne = itemSelected.one()
                await session.delete(itemSelectedOne)
                await session.commit()

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    async def getItemUUIDAuth(self, user_id: int, uri: str) -> list:
        """Gets the items's UUID for authorization in order to
        purge the user's quests

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
                getQuest = select(models.KumikoQuests.uuid).filter(
                    models.KumikoQuests.creator == user_id
                )
                res = await session.execute(getQuest)
                return [row for row in res.scalars()]

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    async def purgeUserQuests(self, user_id: int, uuid: str, uri: str) -> None:
        """Completely purges all of the quests that the user has. This is
        irreversible.

        Args:
            user_id (int): Discord User ID
            uuid (str): Quests Item UUID
            uri (str): Connection URI
        """
        engine = create_async_engine(uri)
        async_session = sessionmaker(
            engine, expire_on_commit=False, class_=AsyncSession
        )
        async with async_session() as session:
            async with session.begin():
                selectAllDelete = (
                    delete(models.KumikoQuests)
                    .filter(models.KumikoQuests.creator == user_id)
                    .filter(models.KumikoQuests.uuid == uuid)
                )
                await session.execute(selectAllDelete)
                await session.commit()

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    async def claimQuest(
        self, user_id: int, claimer_id: int, uuid: str, claimed: bool, uri: str
    ) -> None:
        """Goes ahead and claims the quest

        Args:
            user_id (int): Discord User ID
            claimer_id (int): The Discord User ID of the person who claims it
            uuid (str): Quest Item UUID
            uri (str): Connection URI
        """
        engine = create_async_engine(uri)
        async_session = sessionmaker(
            engine, expire_on_commit=False, class_=AsyncSession
        )
        async with async_session() as session:
            async with session.begin():
                updateQuestItem = (
                    update(
                        models.KumikoQuests,
                        values={
                            models.KumikoQuests.claimed_by: claimer_id,
                            models.KumikoQuests.claimed: claimed,
                        },
                    )
                    .filter(models.KumikoQuests.creator == user_id)
                    .filter(models.KumikoQuests.uuid == uuid)
                )
                await session.execute(updateQuestItem)
                await session.commit()

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    async def viewClaimedQuests(self, claimed: bool, uri: str) -> list:
        """Gets all of the claimed quests

        Args:
            claimed (bool): Whether or not the quest is claimed
            uri (str): Connection URI
        """
        engine = create_async_engine(uri)
        async_session = sessionmaker(
            engine, expire_on_commit=False, class_=AsyncSession
        )
        async with async_session() as session:
            async with session.begin():
                getQuest = select(models.KumikoQuests).filter(
                    models.KumikoQuests.claimed == claimed
                )
                res = await session.execute(getQuest)
                return [row for row in res.scalars()]

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    async def getAllActiveQuests(self, active: bool, uri: str) -> list:
        """Gets all active quests regardless of guilds

        Args:
            active (bool): Quest Active Status
            uri (str): Connection URI

        Returns:
            list: List of results
        """
        engine = create_async_engine(uri)
        async_session = sessionmaker(
            engine, expire_on_commit=False, class_=AsyncSession
        )
        async with async_session() as session:
            async with session.begin():
                selectItem = select(models.KumikoQuests).filter(
                    models.KumikoQuests.active == active
                )
                res = await session.execute(selectItem)
                return [row for row in res.scalars()]

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    async def setQuestActiveStatus(self, uuid: str, active: bool, uri: str) -> None:
        """Sets the quest's active status. This is used to mark the
        quest as active or not

        Args:
            uuid (str): Quest Item UUID
            active (bool): Whether the quests should be active or not
            uri (str): Connection URI
        """
        engine = create_async_engine(uri)
        async_session = sessionmaker(
            engine, expire_on_commit=False, class_=AsyncSession
        )
        async with async_session() as session:
            async with session.begin():
                updateItem = update(
                    models.KumikoQuests, values={models.KumikoQuests.active: active}
                ).filter(models.KumikoQuests.uuid == uuid)
                await session.execute(updateItem)
                await session.commit()

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
