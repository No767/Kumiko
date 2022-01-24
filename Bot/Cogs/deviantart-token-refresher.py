# Note that this cog is disabled since v1.4.4
# This cog has been moved to a separate script
# and docker container
# The source code will still be here for people
# to view it

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

class tokenRefresherUtils:
    def __init__(self):
        self.self = self

    async def get(self):
        meta = MetaData()
        engine = create_async_engine(
            f"postgresql+asyncpg://{Username}:{Password}@{Server_IP}:5432/rin-deviantart-tokens"
        )
        tokens = Table(
            "deviantart-tokens",
            meta,
            Column("Access_Tokens", String),
            Column("Refresh_Tokens", String),
        )
        async with engine.connect() as conn:
            s = tokens.select()
            result_select = await conn.execute(s)
            for row in result_select:
                return row
            
    async def update_values(self, Access_Token, Refresh_Token):
        meta = MetaData()
        engine2 = create_async_engine(
            f"postgresql+asyncpg://{Username}:{Password}@{Server_IP}:5432/rin-deviantart-tokens"
        )
        tokens = Table(
            "deviantart-tokens",
            meta,
            Column("Access_Tokens", String),
            Column("Refresh_Tokens", String),
        )
        async with engine2.begin() as conn2:
            update = tokens.update().values(
                Access_Tokens=f"{Access_Token}", Refresh_Tokens=f"{Refresh_Token}"
            )
            await conn2.execute(update)




class tokenRefresher(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @tasks.loop()
    async def refresher(self):
        tokens = tokenRefresherUtils()
        values = await tokens.get()
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
                print(data)
                Access_token = data["access_token"]
                Refresh_token = data["refresh_token"]
                await tokens.update_values(Access_token, Refresh_token)



def setup(bot):
    bot.add_cog(tokenRefresher(bot))
