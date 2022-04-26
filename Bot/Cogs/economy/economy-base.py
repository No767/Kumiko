import asyncio
import os

import discord
import motor.motor_asyncio
import uvloop
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

Password = os.getenv("MongoDB_Password")
Username = os.getenv("MongoDB_Username")
Server_IP = os.getenv("MongoDB_Server_IP")


# Note: All of these methods are coroutines. They are not regular methods


class ecoBase:
    def __init__(self, ctx):
        self.id = ctx.author.id
        self.gid = ctx.guild.id

    async def get_amount(self):
        client = motor.motor_asyncio.AsyncIOMotorClient(
            f"mongodb://{Username}:{Password}@{Server_IP}:27017"
        )
        db = client.kumiko_economy
        user_data = {"user.discord_id": {"$eq": self.id}, "user.gid": {"$eq": self.gid}}
        eco = db["kumiko_eco"]
        finder = await eco.find_one(user_data)
        if finder is None:
            user_data_insert = {
                "user": {"discord_id": self.id, "gid": self.gid, "coins": 0}
            }
            eco.insert_one(user_data_insert)
        else:
            return finder

    async def set_amount(self, coins):
        setter_client = motor.motor_asyncio.AsyncIOMotorClient(
            f"mongodb://{Username}:{Password}@{Server_IP}:27017"
        )
        database = setter_client.kumiko_economy
        kumiko_eco = database["kumiko_eco"]
        await kumiko_eco.update_one(
            {"user.discord_id": {"$eq": self.id}, "user.gid": {"$eq": self.gid}},
            {"$set": {"user.coins": coins}},
        )


class ecoFunc:
    def __init__(self, ctx):
        self.id = ctx.author.id
        self.gid = ctx.guild.id

    async def balance(self):
        bal_client = motor.motor_asyncio.AsyncIOMotorClient(
            f"mongodb://{Username}:{Password}@{Server_IP}:27017"
        )
        bal_db = bal_client.kumiko_economy
        bal_eco = bal_db["kumiko_eco"]
        data = {"user.discord_id": {"$eq": self.id}}
        return await bal_eco.find_one(data)

    async def top(self):
        grank_client = motor.motor_asyncio.AsyncIOMotorClient(
            f"mongodb://{Username}:{Password}@{Server_IP}:27017"
        )
        grank_db = grank_client.kumiko_economy
        grank_eco = grank_db["kumiko_eco"]
        data1 = [
            {"$match": {"user.discord_id": self.id}},
            {"$group": {"_id": "null", "total": {"$sum": "$user.coins"}}},
            {"$sort": {"coins": -1}},
            {"$limit": 10},
        ]
        async for item in grank_eco.aggregate(data1):
            return item


class Kumiko_EcoV1(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="eco-balance", aliases=["bal"])
    async def user_balance(self, ctx):
        eco = ecoFunc(ctx)
        res = await eco.balance()
        embedVar = discord.Embed()
        embedVar.add_field(
            name="User",
            value=f"{(await self.bot.fetch_user(res['user']['discord_id'])).name}",
            inline=True,
        )
        embedVar.add_field(
            name="Balance", value=f"{res['user']['coins']} coin(s)", inline=True
        )
        await ctx.send(embed=embedVar)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


class Kumiko_EcoV2(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="eco-top", aliases=["top"])
    async def top(self, ctx):
        eco = ecoFunc(ctx)
        eco_top = await eco.top()
        embedVar = discord.Embed()
        embedVar.description = eco_top
        await ctx.send(embed=embedVar)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


def setup(bot):
    bot.add_cog(Kumiko_EcoV1(bot))
