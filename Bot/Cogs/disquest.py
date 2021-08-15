import sqlite3, os, discord, math, random
from Cogs import plugin_tools
from discord.ext import commands
class disaccount:
    def __init__(self, ctx):
        self.id = ctx.author.id
        self.gid = ctx.guild.id

    def getxp(self):
        con = sqlite3.connect("./disquest/user.db")
        cur = con.cursor()
        while True:
            cur.execute(f"SELECT xp FROM user WHERE id = ? AND gid = ?", (self.id, self.gid))
            xp = cur.fetchone()
            if xp == None:
                cur.execute(f"INSERT INTO user (id, gid, xp) VALUES (?, ?, 0)", (self.id, self.gid))
                con.commit()
            else:
                xp = xp[0]
                break
        con.close()
        return xp

    def setxp(self, xp):
        con = sqlite3.connect("./disquest/user.db")
        cur = con.cursor()
        cur.execute(f"UPDATE user SET xp = ? WHERE id = ? AND gid = ?", (xp, self.id, self.gid))
        con.commit()
        cur.close()

    def addxp(self, offset):
        pxp = self.getxp()
        pxp += offset
        self.setxp(pxp)

class lvl:
    def near(xp):
        return round(xp/100)
    def next(xp):
        return math.ceil(xp/100)
    def cur(xp):
        return int(xp/100)

class DisQuest(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        os.chdir(os.path.dirname(__file__))
        con = sqlite3.connect("./disquest/user.db")
        con.execute(f"CREATE TABLE IF NOT EXISTS user (id INTEGER, gid INTEGER, xp INTEGER);")
        con.commit()

    @commands.command(
        name="mylvl",
        help="Displays your activity level!",
    )
    async def mylvl(self, ctx):
        user = disaccount(ctx)
        xp = user.getxp()
        await ctx.channel.send(embed=plugin_tools.fast_embed(
        f"""User: {ctx.author.mention}
        LVL. {lvl.cur(xp)}
        XP {xp}/{lvl.next(xp)*100}"""))

    @commands.command(
        name="rank",
        help="Displays the most active members of your server!"
    )
    async def rank(self, ctx):
        con = sqlite3.connect("./disquest/user.db")
        cur = con.cursor()
        cur.execute(f"SELECT id, xp FROM user WHERE gid = ? ORDER BY xp DESC LIMIT 5", (ctx.guild.id,))
        members = list(cur.fetchall())
        for i, mem in enumerate(members):
            members[i] = f"{i}. {(await self.bot.fetch_user(mem[0])).name} | XP. {mem[1]}\n"
        await ctx.send(embed = plugin_tools.fast_embed(f"**Server Rankings**\n{''.join(members)}"))

    @commands.command(
        name="globalrank",
        help="Displays the most active members of all servers that this bot is connected to!"
    )
    async def grank(self, ctx):
        con = sqlite3.connect("./disquest/user.db")
        cur = con.cursor()
        cur.execute(f"""SELECT id, txp FROM (
            SELECT id, SUM(xp) AS txp FROM user GROUP BY id
        ) ORDER BY txp DESC LIMIT 5""")
        members = list(cur.fetchall())
        for i, mem in enumerate(members):
            members[i] = f"{i}. {(await self.bot.fetch_user(mem[0])).name} | XP. {mem[1]}\n"
        await ctx.send(embed = plugin_tools.fast_embed(f"**Global Rankings**\n{''.join(members)}"))

    @commands.Cog.listener()
    async def on_message(self, ctx):
        if ctx.author.bot: return
        user = disaccount(ctx)
        reward = random.randint(0, 20)
        user.addxp(reward)
        xp = user.getxp()
        if lvl.near(xp) * 100 in range(xp - reward, xp):
            await ctx.channel.send(embed=plugin_tools.fast_embed(f"{ctx.author.mention} has reached LVL. {lvl.cur(xp)}"), delete_after = 20)

def setup(bot):
    bot.add_cog(DisQuest(bot))