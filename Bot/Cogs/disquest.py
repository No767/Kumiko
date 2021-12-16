import math
import os
import random


from discord.ext import commands
import discord
from sqlalchemy import Column, MetaData, Table, create_engine, Integer, select, func

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
        engine = create_engine("sqlite:///Bot/Cogs/disquest/user.db")
        users = Table("user", meta, Column("id", Integer), Column("gid", Integer), Column("xp", Integer))
        conn = engine.connect()
        while True:
            s = select(Column("xp", Integer)).where(users.c.id == self.id, users.c.gid == self.gid)
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
        engine = create_engine("sqlite:///Bot/Cogs/disquest/user.db")
        users = Table("user", meta, Column("id", Integer), Column("gid", Integer), Column("xp", Integer))
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
        os.chdir(os.path.dirname(__file__))
        meta = MetaData()
        engine = create_engine("sqlite:///Bot/Cogs/disquest/user.db")
        Table("user.db", meta, Column("id", Integer), Column("gid", Integer), Column("xp", Integer))
        meta.create_all(engine)
        

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

    @commands.command(
        name="rank", help="Displays the most active members of your server!"
    )
    async def rank(self, ctx):
        meta = MetaData()
        engine = create_engine("sqlite:///Bot/Cogs/disquest/user.db")
        users = Table("user", meta, Column("id", Integer), Column("gid", Integer), Column("xp", Integer))
        conn = engine.connect()
        s = select(Column("id", Integer), Column("xp", Integer)).filter((users.c.gid.is_(myvar))).order_by(
            users.c.xp.desc())
        results = conn.execute(s).fetchall()
        members = list(results.fetchall())
        for i, mem in enumerate(members):
            members[
                i
            ] = f"{i}. {(await self.bot.fetch_user(mem[0])).name} | XP. {mem[1]}\n"
        await ctx.send(
            embed=helper.fast_embed(
                f"**Server Rankings**\n{''.join(members)}")
        )

    @commands.command(
        name="globalrank",
        help="Displays the most active members of all servers that this bot is connected to!",
    )
    async def grank(self, ctx):
        meta = MetaData()
        engine = create_engine("sqlite:///Bot/Cogs/disquest/user.db")
        users = Table("user", meta, Column("id", Integer), Column("gid", Integer), Column("xp", Integer))
        conn = engine.connect()
        s = select(Column("id", Integer), func.sum(users.c.xp).label("txp")).group_by(users.c.id).order_by(
            users.c.xp.desc())
        results = conn.execute(s).fetchall()
        members = list(results)
        for i, mem in enumerate(members):
            members[
                i
            ] = f"{i}. {(await self.bot.fetch_user(mem[0])).name} | XP. {mem[1]}\n"
        await ctx.send(
            embed=helper.fast_embed(
                f"**Global Rankings**\n{''.join(members)}")
        )

    @commands.Cog.listener()
    async def on_message(self, ctx):
        if ctx.author.bot:
            return
        user = disaccount(ctx)
        reward = random.randint(0, 20)
        user.addxp(reward)
        xp = user.getxp()
        if lvl.near(xp) * 100 in range(xp - reward, xp):
            await ctx.channel.send(
                embed=helper.fast_embed(
                    f"{ctx.author.mention} has reached LVL. {lvl.cur(xp)}"
                ),
                delete_after=10,
            )


def setup(bot):
    bot.add_cog(DisQuest(bot))
