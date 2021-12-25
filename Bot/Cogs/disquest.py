import math
import os
import random

import discord
from discord.ext import commands
from dotenv import load_dotenv
from sqlalchemy import (BigInteger, Column, Integer, MetaData, Table,
                        create_engine, func, select)

load_dotenv()

Password = os.getenv("Postgres_Password")
IP = os.getenv("Postgres_Server_IP")
Username = os.getenv("Postgres_Username")


class helper:
    def fast_embed(content):
        colors = [0x8B77BE, 0xA189E2, 0xCF91D1, 0x5665AA, 0xA3A3D2]
        selector = random.choice(colors)
        return discord.Embed(description=content, color=selector)


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
            "user",
            meta,
            Column("id", BigInteger),
            Column("gid", BigInteger),
            Column("xp", Integer),
        )
        conn = engine.connect()
        while True:
            s = select(Column("xp", Integer)).where(
                users.c.id == self.id, users.c.gid == self.gid
            )
            results = conn.execute(s)
            xp = results.fetchone()

            if xp == None:
                ins = users.insert().values(id=self.id, gid=self.gid, xp=0)
                conn.execute(ins)
            else:
                xp = xp[0]
                break
        conn.close()
        return xp

    def setxp(self, xp):
        meta = MetaData()
        engine = create_engine(
            f"postgresql+psycopg2://{Username}:{Password}@{IP}:5432/rin-disquest"
        )
        users = Table(
            "user",
            meta,
            Column("id", BigInteger),
            Column("gid", BigInteger),
            Column("xp", Integer),
        )
        conn = engine.connect()
        update_values = users.update().values(xp=xp, id=self.id, gid=self.gid)
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
        # meta = MetaData()
        # engine = create_engine(
        #     f"postgresql+psycopg2://{Username}:{Password}@{IP}:5432/rin-disquest"
        # )
        # Table(
        #     "user.db",
        #     meta,
        #     Column("id", BigInteger),
        #     Column("gid", BigInteger),
        #     Column("xp", Integer),
        # )
        # meta.create_all(engine)

    @commands.command(
        name="mylvl",
        help="Displays your activity level!",
    )
    async def mylvl(self, ctx):
        user = disaccount(ctx)
        xp = user.getxp()
        await ctx.channel.send(
            embed=helper.fast_embed(
                f"""User: {ctx.author.mention}
        LVL. {lvl.cur(xp)}
        XP {xp}/{lvl.next(xp)*100}"""
            )
        )


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
            "user",
            meta,
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
        embedVar = discord.Embed()
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
            "user",
            meta,
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
        embedVar = discord.Embed()
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
