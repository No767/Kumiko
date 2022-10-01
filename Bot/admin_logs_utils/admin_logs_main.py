import asyncio

import uvloop
from sqlalchemy import select
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
        action_user_id: int,
        user_affected_id: int,
        type_of_action: str,
        reason: str,
        date_issued: str,
        duration: int,
        resolved: bool,
    ) -> None:
        """Adds a row into the AL table

        Args:
            uuid (str): Unique UUID for each row
            guild_id (int): Discord Guild ID
            action_user_id (int): The user who made the action
            user_affected_id (int): The user affected by the action
            type_of_action (str): What was the action (eg a ban, etc)
            reason (str): The reason why
            date_issued (str): Date first issued
            duration (int): Duration of the action
            resolved (bool): Is that action resolved or not
        """
        async with self.asyncSession() as session:
            async with session.begin():
                insertItem = models.AdminLogs(
                    uuid=uuid,
                    guild_id=guild_id,
                    action_user_id=action_user_id,
                    user_affected_id=user_affected_id,
                    type_of_action=type_of_action,
                    reason=reason,
                    date_issued=date_issued,
                    duration=duration,
                    resolved=resolved,
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
                    select(models.AdminLogs).where(
                        models.AdminLogs.guild_id == guild_id
                    )
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
