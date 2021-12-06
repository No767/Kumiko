import asyncio
import os

import aiohttp
import ujson
from discord.ext import commands, tasks
from dotenv import load_dotenv
from sqlalchemy import Column, MetaData, String, Table, create_engine

load_dotenv()

Client_ID = os.getenv("DeviantArt_Client_ID")
Client_Secret = os.getenv("DeviantArt_Client_Secret")


async def select():
    meta = MetaData()
    engine = create_engine("sqlite:///./deviantart-tokens/tokens.db")
    tokens = Table(
        "DA_Tokens",
        meta,
        Column("DA_Access_Tokens", String),
        Column("DA_Refresh_Tokens", String),
    )
    conn = engine.connect()
    s = tokens.select()
    result_select = conn.execute(s)
    for row in result_select:
        return row
    conn.close()


async def update(Access_Token, Refresh_Token):
    meta = MetaData()
    engine = create_engine("sqlite:///./deviantart-tokens/tokens.db")
    tokens = Table(
        "DA_Tokens",
        meta,
        Column("DA_Access_Tokens", String),
        Column("DA_Refresh_Tokens", String),
    )
    conn = engine.connect()
    up = tokens.update().values(
        DA_Access_Tokens=f"{Access_Token}", DA_Refresh_Tokens=f"{Refresh_Token}"
    )
    conn.execute(up)
    conn.close()


class tokenRefresher(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.index = 0
        self.refresher.start()

    @tasks.loop()
    async def refresher(self):
        values = await select()
        Refresh_Token = values[1]
        print(
            f"Current Access Token: {values[0]}\nCurrent Refresh Token: {Refresh_Token}"
        )
        await asyncio.sleep(10)
        async with aiohttp.ClientSession(json_serialize=ujson.dumps) as session:
            params = {
                "client_id": f"{Client_ID}",
                "client_secret": f"{Client_Secret}",
                "grant_type": "refresh_token",
                "refresh_token": f"{Refresh_Token}",
            }
            async with session.get(
                "https://www.deviantart.com/oauth2/token", params=params
            ) as r:
                data = await r.json()
                access_token = data["access_token"]
                refresh_token = data["refresh_token"]
                print(
                    f"New Access Token: {access_token}\nNew Refresh Token: {refresh_token}"
                )
                await asyncio.sleep(3)
                await update(access_token, refresh_token)


def setup(bot):
    bot.add_cog(tokenRefresher(bot))
