import asyncio

import discord
import uvloop
from discord.commands import Option, slash_command
from discord.ext import commands
from economy_utils import KumikoEcoUtils

utilsMain = KumikoEcoUtils()


class ecoAdd(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(
        name="eco-add-item",
        description="Add an item to the marketplace",
        guild_ids=[970159505390325842],
    )
    async def ecoAddItem(
        self,
        ctx,
        *,
        name: Option(str, "The name of the item you wish to add"),
        description: Option(str, "The description of the item you wish to add"),
        amount: Option(int, "The amount you are willing to sell"),
        price: Option(int, "The price of the item")
    ):
        await utilsMain.ins(name, description, amount, price)
        await ctx.respond("Item added to the marketplace")

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


class ecoView(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(name="eco-marketplace-view", description="View the marketplace")
    async def ecoMarketplaceView(self, ctx):
        mainObtain = await utilsMain.obtain()
        filter = ["revision_id", "id", "description", "name"]
        embed = discord.Embed()
        for items in mainObtain:
            mainDict = dict(items)
            for keys, value in mainDict.items():
                if keys not in filter:
                    embed.add_field(name=keys, value=value, inline=True)
                    embed.remove_field(-3)
                embed.title = mainDict["name"]
                embed.description = mainDict["description"]

            await ctx.respond(embed=embed)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


class ecoSearch(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(
        name="eco-marketplace-search",
        description="Search the marketplace",
        guild_ids=[970159505390325842],
    )
    async def ecoMarketplaceSearch(
        self, ctx, *, name: Option(str, "The name of the item you wish to search")
    ):
        mainGetItem = await utilsMain.getItem(name)
        filterTheThird = ["revision_id", "id", "description", "name"]
        embed = discord.Embed()
        print(mainGetItem)
        for (
            k,
            v,
        ) in dict(mainGetItem).items():
            if k not in filterTheThird:
                embed.add_field(name=k, value=v, inline=True)
                embed.remove_field(-2)
            embed.title = dict(mainGetItem)["name"]
            embed.description = dict(mainGetItem)["description"]

        await ctx.respond(embed=embed)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


def setup(bot):
    bot.add_cog(ecoAdd(bot))
    bot.add_cog(ecoView(bot))
    bot.add_cog(ecoSearch(bot))
