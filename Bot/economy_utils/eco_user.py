import asyncio
import os
import uvloop
from dotenv import load_dotenv
from sqlalchemy import (BigInteger, Column, Integer, MetaData, Sequence, Table,
                        func, select)
from sqlalchemy.ext.asyncio import create_async_engine

load_dotenv()

Password = os.getenv("Postgres_Password")
Server_IP = os.getenv("Postgres_Server_IP")
Username = os.getenv("Postgres_Username")


class KumikoEcoUserUtils:
    def __init__(self):
        self.self = self
        
    async def insUserFirstTime(self, user_id: int):
        meta = MetaData()
        engine = create_async_engine(
            f"postgresql+asyncpg://{Username}:{Password}@{Server_IP}:5432/kumiko_eco_users"
        )
        users = Table(
            "users",
            meta,
            Column("user_id", BigInteger),
            Column("coins", Integer),
        )
        async with engine.begin() as conn:
            s = select(users.c.user_id).where(
                users.c.user_id == user_id)
            results = await conn.execute(s)
            results_fetched = results.fetchone()
            if results_fetched is None:
                insert_new = users.insert().values(coins=0, user_id=user_id)
                await conn.execute(insert_new)

    
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
                
    async def updateUser(self, coins: int):
        meta = MetaData()
        engine = create_async_engine(
            f"postgresql+asyncpg://{Username}:{Password}@{Server_IP}:5432/kumiko_eco_users"
        )
        users = Table(
            "users",
            meta,
            Column("user_id", BigInteger),
            Column("coins", Integer),
        )
        async with engine.begin() as conn:
            update_values = (
                users.update()
                .values(coins=coins)
                .filter(users.c.id == self.id)
            )
            await conn.execute(update_values)
        
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
    
    async def initTables(self):
        meta4 = MetaData()
        engine4 = create_async_engine(
            f"postgresql+asyncpg://{Username}:{Password}@{Server_IP}:5432/kumiko_eco_users", echo=True
        )
        Table(
            "users",
            meta4,
            Column("user_id", BigInteger),
            Column("coins", Integer),
        )
        async with engine4.begin() as conn4:
            await conn4.run_sync(meta4.create_all)
            
    async def getUser(self, user_id: int):
        meta = MetaData()
        engine = create_async_engine(
            f"postgresql+asyncpg://{Username}:{Password}@{Server_IP}:5432/kumiko_eco_users"
        )
        users = Table(
            "users",
            meta,
            Column("user_id", BigInteger),
            Column("coins", Integer),
        )
        async with engine.connect() as conn:
            s = users.select(users.c.user_id == user_id)
            result_select = await conn.stream(s)
            async for row in result_select:
                return row
            