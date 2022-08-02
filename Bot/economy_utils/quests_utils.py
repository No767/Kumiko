import asyncio

import uvloop
from sqlalchemy import (BigInteger, Boolean, Column, String, Text, delete,
                        select, update)
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()


class ServerAcctQuests(Base):
    __tablename__ = "server_acct_quests"

    uuid = Column(String, primary_key=True)
    guild_id = Column(BigInteger)
    date_created = Column(String)
    name = Column(String)
    description = Column(Text)
    balance = Column(BigInteger)

    def __iter__(self):
        yield "uuid", self.uuid
        yield "guild_id", self.guild_id
        yield "date_created", self.date_created
        yield "name", self.name
        yield "description", self.description
        yield "balance", self.balance

    def __repr__(self):
        return f"ServerAcctQuests(uuid={self.uuid!r}, guild_id={self.guild_id!r}, date_created={self.date_created!r}, name={self.name!r}, description={self.description!r}, balance={self.balance!r})"


class KumikoQuests(Base):
    __tablename__ = "kumiko_quests"

    uuid = Column(String, primary_key=True)
    guild_id = Column(BigInteger)
    creator = Column(BigInteger)
    date_created = Column(String)
    end_datetime = Column(String)
    name = Column(String)
    description = Column(Text)
    reward = Column(BigInteger)
    active = Column(Boolean)

    def __iter__(self):
        yield "uuid", self.uuid
        yield "guild_id", self.guild_id
        yield "creator", self.creator
        yield "date_created", self.date_created
        yield "end_datetime", self.end_datetime
        yield "name", self.name
        yield "description", self.description
        yield "reward", self.reward
        yield "active", self.active

    def __repr__(self):
        return f"KumikoQuests(uuid={self.uuid!r}, guild_id={self.guild_id!r}, creator={self.creator!r}, date_created={self.date_created!r}, end_datetime={self.end_datetime!r}, name={self.name!r}, description={self.description!r}, reward={self.reward!r}, active={self.active!r})"


class KumikoQuestsUtils:
    def __init__(self):
        self.self = self

    async def initQuestsTables(self, uri: str) -> None:
        """Initializes the tables for Kumiko's Quests system

        Args:
            uri (str): Connection URI
        """
        engine = create_async_engine(uri, echo=True)
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    async def insServerAcct(
        self,
        uuid: str,
        guild_id: int,
        date_created: str,
        name: str,
        description: str,
        balance: int,
        uri: str,
    ) -> None:
        """Inserts data into the server acct

        Args:
            uuid (str): Server Account UUID
            guild_id (int): Discord Guild ID
            date_created (str): The creation date of the server acct
            name (str): Server Acct Name
            description (str): Server Acct Description
            balance (int): Initial Balance
            uri (str): Connection URI
        """
        engine = create_async_engine(uri)
        async_session = sessionmaker(
            engine, expire_on_commit=False, class_=AsyncSession
        )
        async with async_session() as session:
            async with session.begin():
                addItem = ServerAcctQuests(
                    uuid=uuid,
                    guild_id=guild_id,
                    date_created=date_created,
                    name=name,
                    description=description,
                    balance=balance,
                )
                session.add_all([addItem])
                await session.commit()

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    async def getServerAcct(self, guild_id: int, uri: str) -> list:
        """Gets the server account

        Args:
            guild_id (int): Discord Guild ID
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
                selectItem = select(ServerAcctQuests).filter(
                    ServerAcctQuests.guild_id == guild_id
                )
                res = await session.execute(selectItem)
                return [row for row in res.scalars()]

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    async def getServerAcctBal(self, guild_id: int, uri: str) -> list:
        """Gets the server account

        Args:
            guild_id (int): Discord Guild ID
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
                selectItem = select(ServerAcctQuests.balance).filter(
                    ServerAcctQuests.guild_id == guild_id
                )
                res = await session.execute(selectItem)
                return [row for row in res.scalars()]

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    async def updateServerBal(
        self, guild_id: int, uuid: str, balance_amount: int, uri: str
    ) -> None:
        """Updates the amount of Lavender Petals within the server's account

        Args:
            guild_id (int): Discord Guild ID
            uuid (str): Server Account UUID
            balance_amount (int): Amount of Lavender Petals to update to
            uri (str): Connection URI
        """
        engine = create_async_engine(uri)
        async_session = sessionmaker(
            engine, expire_on_commit=False, class_=AsyncSession
        )
        async with async_session() as session:
            async with session.begin():
                updateItemMain = (
                    update(
                        ServerAcctQuests,
                        values={ServerAcctQuests.balance: balance_amount},
                    )
                    .filter(ServerAcctQuests.guild_id == guild_id)
                    .filter(ServerAcctQuests.uuid == uuid)
                )
                await session.execute(updateItemMain)
                await session.commit()

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    async def createQuests(
        self,
        uuid: str,
        guild_id: int,
        creator: int,
        date_created: str,
        end_datetime: str,
        name: str,
        description: str,
        reward: int,
        active: bool,
        uri: str,
    ) -> None:
        """Inserts a new quest into the database

        Args:
            uuid (str): Quests Item UUID
            guild_id (int): Discord Guild ID
            creator (int): Discord User ID of the creator
            date_created (str): The creation date of the quest
            end_datetime (str): The end date and time of the quest
            name (str): Quest Name
            description (str): Quest Description
            reward (int): Quest Reward
            active (bool): Quest Active Status
            uri (str): Connection URI
        """
        engine = create_async_engine(uri)
        async_session = sessionmaker(
            engine, expire_on_commit=False, class_=AsyncSession
        )
        async with async_session() as session:
            async with session.begin():
                addItemQuests = KumikoQuests(
                    uuid=uuid,
                    guild_id=guild_id,
                    creator=creator,
                    date_created=date_created,
                    end_datetime=end_datetime,
                    name=name,
                    description=description,
                    reward=reward,
                    active=active,
                )
                session.add_all([addItemQuests])
                await session.commit()

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    async def getActiveQuests(self, guild_id: int, active: bool, uri: str) -> list:
        """Gets all active quests

        Args:
            guild_id (int): Discord Guild ID
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
                selectItem = (
                    select(KumikoQuests)
                    .filter(KumikoQuests.guild_id == guild_id)
                    .filter(KumikoQuests.active == active)
                )
                res = await session.execute(selectItem)
                return [row for row in res.scalars()]

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    async def getAllQuests(self, guild_id: int, uri: str) -> list:
        """Get all of the quests in the db. Even it is active
        or not

        Args:
            guild_id (int): Discord Guild ID
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
                selectItem = select(KumikoQuests).filter(
                    KumikoQuests.guild_id == guild_id
                )
                res = await session.execute(selectItem)
                return [row for row in res.scalars()]

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    async def updateQuest(
        self, guild_id: int, uuid: str, reward: int, new_end_datetime: str, uri: str
    ) -> None:
        """Updates a quest with the new date and time and

        Args:
            guild_id (int): Discord Guild ID
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
                updateItem = (
                    update(
                        KumikoQuests,
                        values={
                            KumikoQuests.end_datetime: new_end_datetime,
                            KumikoQuests.reward: reward,
                        },
                    )
                    .filter(KumikoQuests.guild_id == guild_id)
                    .filter(KumikoQuests.uuid == uuid)
                )
                await session.execute(updateItem)
                await session.commit()

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    async def getQuestViaName(self, guild_id: int, name: str, uri: str) -> list:
        """Gets the quest via the name

        Args:
            guild_id (int): Discord Guild ID
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
                getQuest = (
                    select(KumikoQuests)
                    .filter(KumikoQuests.guild_id == guild_id)
                    .filter(KumikoQuests.name == name)
                )
                res = await session.execute(getQuest)
                return [row for row in res.scalars()]

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    async def getUserQuestOne(
        self, guild_id: int, user_id: int, name: str, uri: str
    ) -> list:
        """Gets one quest from the user

        Args:
            guild_id (int): Discord Guild ID
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
                    select(KumikoQuests)
                    .filter(KumikoQuests.guild_id == guild_id)
                    .filter(KumikoQuests.creator == user_id)
                    .filter(KumikoQuests.name == name)
                )
                getQuestSelected = await session.scalars(getQuest)
                getQuestSelectedOne = getQuestSelected.first()
                return getQuestSelectedOne

    async def deleteOneQuest(
        self, guild_id: int, user_id: int, uuid: str, uri: str
    ) -> None:
        """Deletes one quest from the DB

        Args:
            guild_id (int): Discord Guild ID
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
                    select(KumikoQuests)
                    .filter(KumikoQuests.guild_id == guild_id)
                    .filter(KumikoQuests.uuid == uuid)
                    .filter(KumikoQuests.creator == user_id)
                )
                itemSelected = await session.scalars(selectOneDelete)
                itemSelectedOne = itemSelected.one()
                await session.delete(itemSelectedOne)
                await session.commit()

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    async def getItemUUIDAuth(self, guild_id: int, user_id: int, uri: str) -> list:
        """Gets the items's UUID for authorization in order to
        purge the user's quests

        Args:
            guild_id (int): Discord Guild ID
            user_id (int): Discord User ID
            uri (str): Connection URI
        """
        engine = create_async_engine(uri)
        async_session = sessionmaker(
            engine, expire_on_commit=False, class_=AsyncSession
        )
        async with async_session() as session:
            async with session.begin():
                getQuest = (
                    select(KumikoQuests.uuid)
                    .filter(KumikoQuests.guild_id == guild_id)
                    .filter(KumikoQuests.creator == user_id)
                )
                res = await session.execute(getQuest)
                return [row for row in res.scalars()]

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    async def purgeUserQuests(
        self, guild_id: int, user_id: int, uuid: str, uri: str
    ) -> None:
        """Completely purges all of the quests that the user has. This is
        irreversible.

        Args:
            guild_id (int): Discord Guild ID
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
                    delete(KumikoQuests)
                    .filter(KumikoQuests.guild_id == guild_id)
                    .filter(KumikoQuests.creator == user_id)
                    .filter(KumikoQuests.uuid == uuid)
                )
                await session.execute(selectAllDelete)
                await session.commit()

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
