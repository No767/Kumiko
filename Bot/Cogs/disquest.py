import math
import os
import random

import discord
from discord.ext import commands
from dotenv import load_dotenv
from sqlalchemy import (BigInteger, Column, Integer, MetaData, Sequence, Table,
                        create_engine, func, select)

load_dotenv()

Password = os.getenv("Postgres_Password")
IP = os.getenv("Postgres_Server_IP")
Username = os.getenv("Postgres_Username")


class disaccount:
    def __init__(self, ctx):
        self.id = ctx.author.id
        self.gid = ctx.guild.id

    def getxp(self):
        meta = MetaData()
        engine = create_engine(
            f"postgresql+psycopg2://{Username}:{Password}@{IP}:5432/rin-disquest"
        )
        users = Table(
            "rin-users-v3",
            meta,
            Column(
                "tracking_id",
                Integer,
                Sequence("tracking_id"),
                primary_key=True,
                autoincrement=True,
            ),
            Column("id", BigInteger),
            Column("gid", BigInteger),
            Column("xp", Integer),
        )
        conn = engine.connect()
        s = select(users.c.xp).where(
            users.c.id == self.id, users.c.gid == self.gid)
        results = conn.execute(s).fetchone()
        if results is None:
            insert_new = users.insert().values(xp=0, id=self.id, gid=self.gid)
            conn.execute(insert_new)
        else:
            for row in results:
                return row
        conn.close()

    def setxp(self, xp):
        meta = MetaData()
        engine = create_engine(
            f"postgresql+psycopg2://{Username}:{Password}@{IP}:5432/rin-disquest"
        )
        users = Table(
            "rin-users-v3",
            meta,
            Column(
                "tracking_id",
                Integer,
                Sequence("tracking_id"),
                primary_key=True,
                autoincrement=True,
            ),
            Column("id", BigInteger),
            Column("gid", BigInteger),
            Column("xp", Integer),
        )
        conn = engine.connect()
        update_values = users.update().values(xp=xp)
        conn.execute(update_values)
        conn.close()

    def addxp(self, offset):
        pxp = self.getxp()
        pxp += offset
        self.setxp(pxp)


class lvl:
    def near(xp):
        return round(xp / 100)

    def next(xp):
        return math.ceil(xp / 100)

    def cur(xp):
        return int(xp / 100)


class DisQuest(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name="mylvl",
        help="Displays your activity level!",
    )
    async def mylvl(self, ctx):
        user = disaccount(ctx)
        xp = user.getxp()
        embedVar = discord.Embed(color=discord.Color.from_rgb(255, 217, 254))
        embedVar.add_field(
            name="User", value=f"{ctx.author.mention}", inline=True)
        embedVar.add_field(name="LVL", value=f"{lvl.cur(xp)}", inline=True)
        embedVar.add_field(
            name="XP", value=f"{xp}/{lvl.next(xp)*100}", inline=True)
        await ctx.send(embed=embedVar)


class DisQuestV2(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name="rank", help="Displays the most active members of your server!"
    )
    async def rank(self, ctx):
        gid = ctx.guild.id
        meta = MetaData()
        engine = create_engine(
            f"postgresql+psycopg2://{Username}:{Password}@{IP}:5432/rin-disquest"
        )
        users = Table(
            "rin-users-v3",
            meta,
            Column(
                "tracking_id",
                Integer,
                Sequence("tracking_id"),
                primary_key=True,
                autoincrement=True,
            ),
            Column("id", BigInteger),
            Column("gid", BigInteger),
            Column("xp", Integer),
        )
        conn = engine.connect()
        s = (
            select(Column("id", BigInteger), Column("xp", Integer))
            .where(users.c.gid == gid)
            .order_by(users.c.xp.desc())
        )
        results = conn.execute(s)
        members = list(results.fetchall())
        for i, mem in enumerate(members):
            members[
                i
            ] = f"{i}. {(await self.bot.fetch_user(mem[0])).name} | XP. {mem[1]}\n"
        embedVar = discord.Embed(color=discord.Color.from_rgb(254, 255, 217))
        embedVar.description = f"**Server Rankings**\n{''.join(members)}"
        await ctx.send(embed=embedVar)


class DisQuestV3(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name="globalrank",
        help="Displays the most active members of all servers that this bot is connected to!",
        aliases=["grank"],
    )
    async def grank(self, ctx):
        meta = MetaData()
        engine = create_engine(
            f"postgresql+psycopg2://{Username}:{Password}@{IP}:5432/rin-disquest"
        )
        users = Table(
            "rin-users-v3",
            meta,
            Column(
                "tracking_id",
                Integer,
                Sequence("tracking_id"),
                primary_key=True,
                autoincrement=True,
            ),
            Column("id", BigInteger),
            Column("gid", BigInteger),
            Column("xp", Integer),
        )
        conn = engine.connect()
        s = (
            select(Column("id", Integer), func.sum(users.c.xp).label("txp"))
            .group_by(users.c.id)
            .group_by(users.c.xp)
            .order_by(users.c.xp.desc())
        )
        results = conn.execute(s).fetchall()
        members = list(results)
        for i, mem in enumerate(members):
            members[
                i
            ] = f"{i}. {(await self.bot.fetch_user(mem[0])).name} | XP. {mem[1]}\n"
        embedVar = discord.Embed(color=discord.Color.from_rgb(217, 255, 251))
        embedVar.description = f"**Global Rankings**\n{''.join(members)}"
        await ctx.send(embed=embedVar)


class DisQuestV4(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, ctx):
        if ctx.author.bot:
            return
        user = disaccount(ctx)
        reward = random.randint(0, 20)
        user.addxp(reward)


def setup(bot):
    bot.add_cog(DisQuest(bot))
    bot.add_cog(DisQuestV2(bot))
    bot.add_cog(DisQuestV3(bot))
    bot.add_cog(DisQuestV4(bot))
