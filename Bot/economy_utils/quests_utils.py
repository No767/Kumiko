import asyncio

import uvloop
from sqlalchemy import BigInteger, Boolean, Column, String, Text, select
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()


class ServerAcctQuests(Base):
    __tablename__ = "server_acct_quests"

    guild_id = Column(BigInteger, primary_key=True)
    uuid = Column(String)
    date_created = Column(String)
    name = Column(String)
    description = Column(Text)
    balance = Column(BigInteger)

    def __iter__(self):
        yield "guild_id", self.guild_id
        yield "uuid", self.uuid
        yield "date_created", self.date_created
        yield "name", self.name
        yield "description", self.description
        yield "balance", self.balance

    def __repr__(self):
        return f"ServerAcctQuests(guild_id={self.guild_id!r}, uuid={self.uuid!r}, date_created={self.date_created!r}, name={self.name!r}, description={self.description!r}, balance={self.balance!r})"


class KumikoQuests(Base):
    __tablename__ = "kumiko_quests"

    guild_id = Column(BigInteger, primary_key=True)
    uuid = Column(String)
    creator = Column(BigInteger)
    date_created = Column(String)
    end_date = Column(String)
    name = Column(String)
    description = Column(Text)
    reward = Column(BigInteger)
    active = Column(Boolean)

    def __iter__(self):
        yield "guild_id", self.guild_id
        yield "uuid", self.uuid
        yield "creator", self.creator
        yield "date_created", self.date_created
        yield "end_date", self.end_date
        yield "name", self.name
        yield "description", self.description
        yield "reward", self.reward
        yield "active", self.active

    def __repr__(self):
        return f"KumikoQuests(guild_id={self.guild_id!r}, uuid={self.uuid!r}, creator={self.creator!r}, date_created={self.date_created!r}, end_date={self.end_date!r}, name={self.name!r}, description={self.description!r}, reward={self.reward!r}, active={self.active!r})"


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
        guild_id: int,
        uuid: str,
        date_created: str,
        name: str,
        description: str,
        balance: int,
        uri: str,
    ) -> None:
        """Inserts data into the server acct

        Args:
            guild_id (int): Discord Guild ID
            uuid (str): Server Account UUID
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
                    guild_id=guild_id,
                    uuid=uuid,
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
