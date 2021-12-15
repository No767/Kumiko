import asyncio
import os

import aiohttp
import ujson
from discord.ext import commands, tasks
from dotenv import load_dotenv
from sqlalchemy import Column, MetaData, String, Table, create_engine, text

load_dotenv()

Client_ID = os.getenv("DeviantArt_Client_ID")
Client_Secret = os.getenv("DeviantArt_Client_Secret")


def select():
    meta = MetaData()
    engine = create_engine("sqlite:///Bot/Cogs/daTokens/tokens.db")
    tokens = Table("DA_Tokens", meta, Column("Access_Tokens", String), Column("Refresh_Tokens", String))
    s = tokens.select()
    conn = engine.connect()
    result_select = conn.execute(s)
    for row in result_select:
        return row


def update(Access_Token, Refresh_Token):
    meta = MetaData()
    engine = create_engine("sqlite:///Bot/Cogs/daTokens/tokens.db")
    tokens = Table("DA_Tokens", meta, Column("Access_Tokens", String), Column("Refresh_Tokens", String))
    conn = engine.connect()
    update = tokens.update().values(
        Access_Tokens=f"{Access_Token}", Refresh_Tokens=f"{Refresh_Token}"
    )
    conn.execute(update)


class tokenRefresher(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.refresher.start()

    @tasks.loop()
    async def refresher(self):
        values = select()
        Refresh_Token = values[1]
        await asyncio.sleep(3300)
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
                update(access_token, refresh_token)


def setup(bot):
    bot.add_cog(tokenRefresher(bot))
