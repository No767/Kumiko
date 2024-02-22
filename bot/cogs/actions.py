import discord
import orjson
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Greedy
from kumikocore import KumikoCore
from libs.utils import Embed
from libs.utils.context import KContext


class Actions(commands.Cog):
    """Hug, pet, or kiss someone on Discord"""

    def __init__(self, bot: KumikoCore) -> None:
        self.bot = bot
        self.session = self.bot.session

    @property
    def display_emoji(self) -> discord.PartialEmoji:
        return discord.PartialEmoji.from_str("<:headpat:1020641548645437491>")

    def format_greedy(self, list: list[str]) -> str:
        """Formats a Greedy list into a human-readable string

        For example, if we had a list of ["a", "b", "c"], it would return "a, b, and c".
        If we had a list of ["a", "b"], it would return "a and b".
        If we had a list of ["a"], it would return "a".
        If we had a list of [], it would return "".

        Args:
            list: The list of strings to format

        Returns:
            str: The formatted string
        """
        if len(list) >= 3:
            return f"{', '.join(list[:-1])}, and {list[-1]}"
        elif len(list) == 2:
            return " and ".join(list)
        return "".join(list)

    @commands.hybrid_command(name="hug")
    @app_commands.describe(user="The user to hug")
    async def hug(self, ctx: KContext, user: Greedy[discord.Member]) -> None:
        """Hug someone on Discord!"""
        async with self.session.get("https://nekos.life/api/v2/img/hug") as r:
            data = await r.json(loads=orjson.loads)
            embed = Embed(
                title=f"{ctx.author.name} hugs {self.format_greedy([items.name for items in user])}!"
            )
            embed.set_image(url=data["url"])
            await ctx.send(embed=embed)

    @commands.hybrid_command(name="pat")
    @app_commands.describe(user="The user to pat")
    async def pat(self, ctx: KContext, user: Greedy[discord.Member]) -> None:
        """Give someone a headpat!"""
        async with self.session.get("https://nekos.life/api/v2/img/pat") as r:
            data = await r.json(loads=orjson.loads)
            embed = Embed(
                title=f"{ctx.author.name} pats {self.format_greedy([items.name for items in user])}!"
            )
            embed.set_image(url=data["url"])
            await ctx.send(embed=embed)

    @commands.hybrid_command(name="kiss")
    @app_commands.describe(user="The user to kiss")
    async def kiss(self, ctx: KContext, user: Greedy[discord.Member]) -> None:
        """Give someone a kiss!"""
        async with self.session.get("https://nekos.life/api/v2/img/kiss") as r:
            data = await r.json(loads=orjson.loads)
            embed = Embed(
                title=f"{ctx.author.name} kisses {self.format_greedy([items.name for items in user])}!"
            )
            embed.set_image(url=data["url"])
            await ctx.send(embed=embed)

    @commands.hybrid_command(name="cuddle")
    @app_commands.describe(user="The user to cuddle")
    async def cuddle(self, ctx: KContext, user: Greedy[discord.Member]) -> None:
        """Cuddle someone on Discord!"""
        async with self.session.get("https://nekos.life/api/v2/img/cuddle") as r:
            data = await r.json(loads=orjson.loads)
            embed = Embed(
                title=f"{ctx.author.name} cuddles {self.format_greedy([items.name for items in user])}!"
            )
            embed.set_image(url=data["url"])
            await ctx.send(embed=embed)

    @commands.hybrid_command(name="slap")
    @app_commands.describe(user="The user to slap")
    async def slap(self, ctx: KContext, user: Greedy[discord.Member]) -> None:
        """Slaps someone on Discord!"""
        async with self.session.get("https://nekos.life/api/v2/img/slap") as r:
            data = await r.json(loads=orjson.loads)
            embed = Embed(
                title=f"{ctx.author.name} slaps {self.format_greedy([items.name for items in user])}!"
            )
            embed.set_image(url=data["url"])
            await ctx.send(embed=embed)

    @commands.hybrid_command(name="tickle")
    @app_commands.describe(user="The user to tickle")
    async def tickles(self, ctx: KContext, user: Greedy[discord.Member]) -> None:
        """Tickle someone on Discord!"""
        async with self.session.get("https://nekos.life/api/v2/img/tickle") as r:
            data = await r.json(loads=orjson.loads)
            embed = Embed(
                title=f"{ctx.author.name} tickles {self.format_greedy([items.name for items in user])}!"
            )
            embed.set_image(url=data["url"])
            await ctx.send(embed=embed)

    @commands.hybrid_command(name="poke")
    @app_commands.describe(user="The user to poke")
    async def poke(self, ctx: KContext, user: Greedy[discord.Member]) -> None:
        """Poke someone on Discord!"""
        async with self.session.get("https://nekos.life/api/v2/img/poke") as r:
            data = await r.json(loads=orjson.loads)
            embed = Embed(
                title=f"{ctx.author.name} pokes {self.format_greedy([items.name for items in user])}!"
            )
            embed.set_image(url=data["url"])
            await ctx.send(embed=embed)


async def setup(bot: KumikoCore) -> None:
    await bot.add_cog(Actions(bot))
