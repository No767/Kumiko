import aiohttp
import discord
import orjson
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Greedy
from Libs.utils import Embed, formatGreedy


class Actions(commands.Cog):
    """Hug, pet, or kiss someone on Discord!"""

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.hybrid_command(name="hug")
    @app_commands.describe(user="The user to hug")
    async def hug(self, ctx: commands.Context, user: Greedy[discord.Member]) -> None:
        """Hug someone on Discord!"""
        async with aiohttp.ClientSession() as session:
            async with session.get("https://nekos.life/api/v2/img/hug") as r:
                data = await r.json(loads=orjson.loads)
                embed = Embed(
                    title=f"{ctx.author.name} hugs {formatGreedy([items.name for items in user])}!"
                )
                embed.set_image(url=data["url"])
                await ctx.send(embed=embed)

    @commands.hybrid_command(name="pat")
    @app_commands.describe(user="The user to pat")
    async def pat(self, ctx: commands.Context, user: Greedy[discord.Member]) -> None:
        """Give someone a headpat!"""
        async with aiohttp.ClientSession() as session:
            async with session.get("https://nekos.life/api/v2/img/pat") as r:
                data = await r.json(loads=orjson.loads)
                embed = Embed(
                    title=f"{ctx.author.name} pats {formatGreedy([items.name for items in user])}!"
                )
                embed.set_image(url=data["url"])
                await ctx.send(embed=embed)

    @commands.hybrid_command(name="kiss")
    @app_commands.describe(user="The user to kiss")
    async def kiss(self, ctx: commands.Context, user: Greedy[discord.Member]) -> None:
        """Give someone a kiss!"""
        async with aiohttp.ClientSession() as session:
            async with session.get("https://nekos.life/api/v2/img/kiss") as r:
                data = await r.json(loads=orjson.loads)
                embed = Embed(
                    title=f"{ctx.author.name} kisses {formatGreedy([items.name for items in user])}!"
                )
                embed.set_image(url=data["url"])
                await ctx.send(embed=embed)

    @commands.hybrid_command(name="cuddle")
    @app_commands.describe(user="The user to cuddle")
    async def cuddle(self, ctx: commands.Context, user: Greedy[discord.Member]) -> None:
        """Cuddle someone on Discord!"""
        async with aiohttp.ClientSession() as session:
            async with session.get("https://nekos.life/api/v2/img/cuddle") as r:
                data = await r.json(loads=orjson.loads)
                embed = Embed(
                    title=f"{ctx.author.name} cuddles {formatGreedy([items.name for items in user])}!"
                )
                embed.set_image(url=data["url"])
                await ctx.send(embed=embed)

    @commands.hybrid_command(name="slap")
    @app_commands.describe(user="The user to slap")
    async def slap(self, ctx: commands.Context, user: Greedy[discord.Member]) -> None:
        """Slaps someone on Discord!"""
        async with aiohttp.ClientSession() as session:
            async with session.get("https://nekos.life/api/v2/img/slap") as r:
                data = await r.json(loads=orjson.loads)
                embed = Embed(
                    title=f"{ctx.author.name} slaps {formatGreedy([items.name for items in user])}!"
                )
                embed.set_image(url=data["url"])
                await ctx.send(embed=embed)

    @commands.hybrid_command(name="tickle")
    @app_commands.describe(user="The user to tickle")
    async def tickles(
        self, ctx: commands.Context, user: Greedy[discord.Member]
    ) -> None:
        """Tickle someone on Discord!"""
        async with aiohttp.ClientSession() as session:
            async with session.get("https://nekos.life/api/v2/img/tickle") as r:
                data = await r.json(loads=orjson.loads)
                embed = Embed(
                    title=f"{ctx.author.name} tickles {formatGreedy([items.name for items in user])}!"
                )
                embed.set_image(url=data["url"])
                await ctx.send(embed=embed)

    @commands.hybrid_command(name="poke")
    @app_commands.describe(user="The user to poke")
    async def poke(self, ctx: commands.Context, user: Greedy[discord.Member]) -> None:
        """Poke someone on Discord!"""
        async with aiohttp.ClientSession() as session:
            async with session.get("https://nekos.life/api/v2/img/poke") as r:
                data = await r.json(loads=orjson.loads)
                embed = Embed(
                    title=f"{ctx.author.name} pokes {formatGreedy([items.name for items in user])}!"
                )
                embed.set_image(url=data["url"])
                await ctx.send(embed=embed)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Actions(bot))
