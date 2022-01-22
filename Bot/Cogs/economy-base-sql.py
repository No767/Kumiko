import discord 
import asyncio
import uvloop
from sqlalchemy import (BigInteger, Column, Integer, MetaData, Sequence, Table,
                        func, select)
from sqlalchemy.ext.asyncio import create_async_engine
from discord.ext import commands
import os

from dotenv import load_dotenv

load_dotenv()

Password = os.getenv("Postgres_Password")
Server_IP = os.getenv("Postgres_Server_IP")
Username = os.getenv("Postgres_Username")

class kumikoEcoUtils:
    def __init__(self, ctx):
        self.id = 454357482102587393 # ctx.author.id
        self.gid = 866199405090308116 # ctx.guild.id
        
    async def get_amount(self):
        meta = MetaData()
        users = Table("kumiko-users", meta, Column("id", BigInteger), Column("gid", BigInteger),
                      Column("coins", Integer))
        engine = create_async_engine(f"postgresql+asyncpg://{Username}:{Password}@{Server_IP}:5432/kumiko-eco")
        async with engine.connect() as conn:
            s = select(users.c.coins).where(users.c.id == self.id, users.c.gid == self.gid)
            res = await conn.execute(s)
            res_fetched = res.fetchone()
            if res_fetched is None:
                insert_new = users.insert().values(coins=0, id=self.id, gid=self.gid)
                await conn.execute(insert_new)
            else:
                for row in res_fetched:
                    return row
                
    async def set_amount(self, coins):
        meta = MetaData()
        users = Table("kumiko-users", meta, Column("id", BigInteger), Column("gid", BigInteger),
                      Column("coins", Integer))
        engine2 = create_async_engine(f"postgresql+asyncpg://{Username}:{Password}@{Server_IP}:5432/kumiko-eco")
        async with engine2.begin() as conn2:
            update_values = users.update().values(coins=coins).filter(users.c.id == self.id).filter(users.c.gid == self.gid)
            await conn2.execute(update_values)