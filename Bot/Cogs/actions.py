import asyncio

import aiohttp
import discord
import orjson
from discord.ext import commands
from Libs.utils import Embed


class Actions(commands.Cog):
    """Hug, pet, or kiss someone on Discord!"""

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.hybrid_command(name="hug")
    async def hug(self, ctx: commands.Context, user: discord.Member) -> None:
        """Hug someone on Discord!

        Args:
            ctx (commands.Context): The context of the command.
            user (discord.Member): The user to hug
        """
        print(asyncio.get_event_loop_policy())
        async with aiohttp.ClientSession() as session:
            async with session.get("https://nekos.life/api/v2/img/hug") as r:
                data = await r.json(loads=orjson.loads)
                embed = Embed(title=f"{ctx.author.name} hugs {user.name}!")
                embed.set_image(url=data["url"])
                await ctx.send(embed=embed)

    @commands.hybrid_command(name="pat")
    async def pat(self, ctx: commands.Context, user: discord.Member) -> None:
        """Give someone a headpat!

        Args:
            ctx (commands.Context): Context of the command
            user (discord.Member): The user to hug
        """
        async with aiohttp.ClientSession() as session:
            async with session.get("https://nekos.life/api/v2/img/pat") as r:
                data = await r.json(loads=orjson.loads)
                embed = Embed(title=f"{ctx.author.name} pats {user.name}!")
                embed.set_image(url=data["url"])
                await ctx.send(embed=embed)

    @commands.hybrid_command(name="kiss")
    async def kiss(self, ctx: commands.Context, user: discord.Member) -> None:
        """Give someone a kiss!

        Args:
            ctx (commands.Context): Context of the command
            user (discord.Member): The user to kiss
        """
        async with aiohttp.ClientSession() as session:
            async with session.get("https://nekos.life/api/v2/img/kiss") as r:
                data = await r.json(loads=orjson.loads)
                embed = Embed(title=f"{ctx.author.name} kisses {user.name}!")
                embed.set_image(url=data["url"])
                await ctx.send(embed=embed)

    @commands.hybrid_command(name="cuddle")
    async def cuddle(self, ctx: commands.Context, user: discord.Member) -> None:
        """Cuddle someone on Discord!

        Args:
            ctx (commands.Context): Context of the command
            user (discord.Member): The user to cuddle
        """
        async with aiohttp.ClientSession() as session:
            async with session.get("https://nekos.life/api/v2/img/cuddle") as r:
                data = await r.json(loads=orjson.loads)
                embed = Embed(title=f"{ctx.author.name} cuddles {user.name}!")
                embed.set_image(url=data["url"])
                await ctx.send(embed=embed)

    @commands.hybrid_command(name="slap")
    async def slap(self, ctx: commands.Context, user: discord.Member) -> None:
        """Slaps someone on Discord!

        Args:
            ctx (commands.Context): Context of the command
            user (discord.Member): The user to slap
        """
        async with aiohttp.ClientSession() as session:
            async with session.get("https://nekos.life/api/v2/img/slap") as r:
                data = await r.json(loads=orjson.loads)
                embed = Embed(title=f"{ctx.author.name} slaps {user.name}!")
                embed.set_image(url=data["url"])
                await ctx.send(embed=embed)

    @commands.hybrid_command(name="tickle")
    async def tickles(self, ctx: commands.Context, user: discord.Member) -> None:
        """Tickle someone on Discord!

        Args:
            ctx (commands.Context): Context of the command
            user (discord.Member): The user to tickle
        """
        async with aiohttp.ClientSession() as session:
            async with session.get("https://nekos.life/api/v2/img/tickle") as r:
                data = await r.json(loads=orjson.loads)
                embed = Embed(title=f"{ctx.author.name} tickles {user.name}!")
                embed.set_image(url=data["url"])
                await ctx.send(embed=embed)

    @commands.hybrid_command(name="poke")
    async def poke(self, ctx: commands.Context, user: discord.Member) -> None:
        """Poke someone on Discord!

        Args:
            ctx (commands.Context): Context of the command
            user (discord.Member): The user to poke
        """
        async with aiohttp.ClientSession() as session:
            async with session.get("https://nekos.life/api/v2/img/poke") as r:
                data = await r.json(loads=orjson.loads)
                embed = Embed(title=f"{ctx.author.name} pokes {user.name}!")
                embed.set_image(url=data["url"])
                await ctx.send(embed=embed)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Actions(bot))
