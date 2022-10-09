import asyncio
from typing import Union

import uvloop
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from . import models
from .models import Base


class KumikoAdminLogsUtils:
    def __init__(self, uri: str):
        """Constructor for the KumikoAdminLogsUtils class.

        This takes an parameter `uri`, which is used to connect to the database.

        Args:
            uri (str): Connection URI
        """
        self.self = self
        self.uri = uri
        self.engine = create_async_engine(self.uri)
        self.asyncSession = sessionmaker(
            self.engine, expire_on_commit=False, class_=AsyncSession
        )

    async def initAllALTables(self) -> None:
        """Initializes all of the tables needed for AL"""
        engine = create_async_engine(self.uri)
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    async def addALRow(
        self,
        uuid: str,
        guild_id: int,
        action_user_name: str,
        user_affected_name: str,
        type_of_action: str,
        reason: Union[str, None],
        date_issued: str,
        duration: int,
        datetime_duration: Union[str, None],
    ) -> None:
        """Adds a row into the AL table

        This makes a DB transaction, and just adds it as a row. Each ban, kick, etc will use this

        Args:
            uuid (str): Unique UUID for each row
            guild_id (int): Discord Guild ID
            type_of_action (str): What was the action (eg a ban, etc)
            reason (Union[str, None]): The reason why
            date_issued (str): Date first issued
            duration (int): Duration of the action
            datetime_duration (Union[str, None]): The date's duration. If used for timeouts, this will be set to a ISO-8601 string. But for any others, this will be `None`
        """
        async with self.asyncSession() as session:
            async with session.begin():
                insertItem = models.AdminLogs(
                    uuid=uuid,
                    guild_id=guild_id,
                    type_of_action=type_of_action,
                    action_user_name=action_user_name,
                    user_affected_name=user_affected_name,
                    reason=reason,
                    date_issued=date_issued,
                    duration=duration,
                    datetime_duration=datetime_duration,
                )
                session.add_all([insertItem])
                await session.commit()

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    async def selAllGuildRows(self, guild_id: int) -> list:
        """Gets all of the rows where it matches the guild_id

        Args:
            guild_id (int): Discord Guild ID

        Returns:
            list: A `list` of `models.AdminLogs` objects
        """
        async with self.asyncSession() as session:
            async with session.begin():
                rows = await session.execute(
                    select(models.AdminLogs)
                    .where(models.AdminLogs.guild_id == guild_id)
                    .order_by(models.AdminLogs.type_of_action.asc())
                )
                return rows.scalars().all()

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    async def selAction(self, type_of_action: str, guild_id: int) -> list:
        """Based on a type of action, search and return that result

        Args:
            type_of_action (str): What action was done (eg a ban, kick, etc)
            guild_id (int): Discord Guild ID

        Returns:
            list: A `list` of `models.AdminLogs` objects
        """
        async with self.asyncSession() as session:
            async with session.begin():
                rows = await session.execute(
                    select(models.AdminLogs)
                    .where(models.AdminLogs.type_of_action == type_of_action)
                    .where(models.AdminLogs.guild_id == guild_id)
                )
                return rows.scalars().all()

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    async def purgeData(self, guild_id: int) -> None:
        """Purges all of the admin log data for the specified guild

        Once the data has been purged, there is no going back...

        Args:
            guild_id (int): Discord Guild ID
        """
        async with self.asyncSession() as session:
            async with session.begin():
                await session.execute(
                    delete(models.AdminLogs).where(
                        models.AdminLogs.guild_id == guild_id
                    )
                )
                await session.commit()

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
