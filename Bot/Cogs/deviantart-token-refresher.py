import asyncio
import os

import aiohttp
import orjson
from discord.ext import commands, tasks
from dotenv import load_dotenv
from sqlalchemy import Column, MetaData, String, Table
from sqlalchemy.ext.asyncio import create_async_engine

load_dotenv()

Client_ID = os.getenv("DeviantArt_Client_ID")
Client_Secret = os.getenv("DeviantArt_Client_Secret")
Password = os.getenv("Postgres_Password")
Server_IP = os.getenv("Postgres_Server_IP")
Username = os.getenv("Postgres_Username")


async def select_values():
    meta = MetaData()
    engine = create_async_engine(
        f"postgresql+asyncpg://{Username}:{Password}@{Server_IP}:5432/rin-deviantart-tokens"
    )
    tokens = Table(
        "DA_Tokens",
        meta,
        Column("Access_Tokens", String),
        Column("Refresh_Tokens", String),
    )
    async with engine.connect() as conn:
        s = tokens.select()
        result_select = await conn.execute(s)
        for row in result_select:
            return row
        await conn.close()


async def update_values(Access_Token, Refresh_Token):
    meta = MetaData()
    engine = create_async_engine(
        f"postgresql+asyncpg://{Username}:{Password}@{Server_IP}:5432/rin-deviantart-tokens"
    )
    tokens = Table(
        "DA_Tokens",
        meta,
        Column("Access_Tokens", String),
        Column("Refresh_Tokens", String),
    )
    async with engine.connect() as conn:
        update = tokens.update().values(
            Access_Tokens=f"{Access_Token}", Refresh_Tokens=f"{Refresh_Token}"
        )
        await conn.execute(update)
        await conn.close()


class tokenRefresher(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.refresher.start()

    @tasks.loop()
    async def refresher(self):
        values = await select_values()
        Refresh_Token_Select = values[1]
        await asyncio.sleep(3300)
        async with aiohttp.ClientSession(json_serialize=orjson.dumps) as session:
            params = {
                "client_id": f"{Client_ID}",
                "client_secret": f"{Client_Secret}",
                "grant_type": "refresh_token",
                "refresh_token": f"{Refresh_Token_Select}",
            }
            async with session.get(
                "https://www.deviantart.com/oauth2/token", params=params
            ) as r:
                data = await r.json()
                Access_token = data["access_token"]
                Refresh_token = data["refresh_token"]
                await update_values(Access_token, Refresh_token)


def setup(bot):
    bot.add_cog(tokenRefresher(bot))
