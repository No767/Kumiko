import asyncio
import os

import aiohttp
import ujson
from discord.ext import commands, tasks
from dotenv import load_dotenv
from sqlalchemy import MetaData, Table, create_engine

load_dotenv()

Client_ID = os.getenv("DeviantArt_Client_ID")
Client_Secret = os.getenv("DeviantArt_Client_Secret")


def select():
    meta = MetaData()
    engine = create_engine("sqlite:///tokens.db", echo=True)
    tokens = Table(
        "DeviantArt_Tokens",
        meta,
        autoload_with=engine,
        autoload=True
    )
    meta.create_all(engine, bind=engine)
    with engine.connect() as conn:
        s = tokens.select()
        result_select = conn.execute(s)
        for row in result_select:
            return row


def update(Access_Token, Refresh_Token):
    meta = MetaData()
    engine = create_engine("sqlite:///tokens.db", echo=True)
    tokens = Table(
        "DeviantArt_Tokens",
        meta,
        autoload_with=engine,
        autoload=True
    )
    meta.create_all(engine, bind=engine, tables=tokens)
    meta.reflect(bind=engine)
    with engine.connect() as conn:
        up = tokens.update().values(
            DA_Access_Tokens=f"{Access_Token}", DA_Refresh_Tokens=f"{Refresh_Token}"
        )
        conn.execute(up)


class tokenRefresher(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.index = 0
        self.refresher.start()
        
    @tasks.loop()
    async def refresher(self):
        print("yes")
        values = select()
        Refresh_Token = values[1]
        print(f"Current Access Token: {values[0]}\nCurrent Refresh Token: {values[1]}\n")
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
                print(f"New Access Token: {access_token}\nNew Refresh Token: {refresh_token}\n")
                await asyncio.sleep(3)
                update(access_token, refresh_token)
    


def setup(bot):
    bot.add_cog(tokenRefresher(bot))
