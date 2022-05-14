import asyncio
from datetime import datetime

import discord
import uvloop
from discord.commands import Option, SlashCommandGroup
from discord.ext import commands, pages
from economy_utils import KumikoEcoUtils

utilsMain = KumikoEcoUtils()
today = datetime.now()


class ecoMarketplace(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    eco_marketplace = SlashCommandGroup(
        name="marketplace",
        description="Commands for Kumiko's Marketplace",
        guild_ids=[970159505390325842],
    )

    @eco_marketplace.command(name="add-item")
    async def ecoAddItem(
        self,
        ctx,
        *,
        name: Option(str, "The name of the item you wish to add"),
        description: Option(str, "The description of the item you wish to add"),
        amount: Option(int, "The amount you are willing to sell"),
        price: Option(int, "The price of the item"),
    ):
        """Adds an item into the marketplace"""
        dateEntry = today.strftime("%B %d, %Y %H:%M:%S")
        owner = ctx.user.id
        await utilsMain.ins(dateEntry, owner, name, description, amount, price)
        await ctx.respond("Item added to the marketplace")

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    @eco_marketplace.command(name="view")
    async def ecoMarketplaceView(self, ctx):
        """View the marketplace"""
        mainObtain = await utilsMain.obtain()
        paginator = pages.Paginator(
            pages=[
                discord.Embed(
                    title=dict(items)["name"], description=dict(items)["description"]
                )
                .add_field(name="Amount", value=dict(items)["amount"], inline=True)
                .add_field(name="Price", value=dict(items)["price"], inline=True)
                .add_field(name="Date Added", value=dict(items)["date_added"])
                .add_field(
                    name="Owner",
                    value=f"{await self.bot.fetch_user(dict(items)['owner'])}",
                )
                for items in mainObtain
            ],
        )
        await paginator.respond(ctx.interaction, ephemeral=False)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    @eco_marketplace.command(
        name="search",
    )
    async def ecoMarketplaceSearch(
        self, ctx, *, name: Option(str, "The name of the item you wish to search")
    ):
        """Search the marketplace"""
        mainGetItem = await utilsMain.getItem(name)
        paginator = pages.Paginator(
            pages=[
                discord.Embed(
                    title=dict(item)["name"], description=dict(item)["description"]
                )
                .add_field(name="Amount", value=dict(item)["amount"], inline=True)
                .add_field(name="Price", value=dict(item)["price"], inline=True)
                .add_field(name="Date Added", value=dict(item)["date_added"])
                .add_field(
                    name="Owner",
                    value=f"{await self.bot.fetch_user(dict(item)['owner'])}",
                )
                for item in mainGetItem
            ]
        )
        await paginator.respond(ctx.interaction, ephemeral=False)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


def setup(bot):
    bot.add_cog(ecoMarketplace(bot))
