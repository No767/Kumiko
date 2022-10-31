import asyncio
import os
import uuid
from datetime import datetime

import discord
import motor.motor_asyncio
import uvloop
from beanie import init_beanie
from dateutil import parser
from discord.commands import Option, SlashCommandGroup
from discord.ext import commands, pages
from dotenv import load_dotenv
from economy_utils import (
    KumikoEcoUserUtils,
    KumikoEcoUtils,
    KumikoUserInvUtils,
    MarketplaceModel,
)
from kumiko_ui_components import (
    MarketplaceAddItem,
    MarketplaceDeleteOneItem,
    MarketplacePurgeAllView,
    MarketplaceUpdateAmount,
    MarketplaceUpdateItemPrice,
)
from rin_exceptions import NoItemsError

load_dotenv()

POSTGRES_PASSWORD = os.getenv("Postgres_Password")
POSTGRES_SERVER_IP = os.getenv("Postgres_Server_IP")
POSTGRES_DATABASE = os.getenv("Postgres_Kumiko_Database")
POSTGRES_USERNAME = os.getenv("Postgres_Username")
POSTGRES_SERVER_PORT = os.getenv("Postgres_Port")
MONGODB_PASSWORD = os.getenv("MongoDB_Password")
MONGODB_USERNAME = os.getenv("MongoDB_Username")
MONGODB_SERVER_IP = os.getenv("MongoDB_Server_IP")
MONGODB_PORT = os.getenv("MongoDB_Server_Port")

USERS_CONNECTION_URI = f"postgresql+asyncpg://{POSTGRES_USERNAME}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER_IP}:{POSTGRES_SERVER_PORT}/{POSTGRES_DATABASE}"
MARKETPLACE_CONNECTION_URI = f"mongodb://{MONGODB_USERNAME}:{MONGODB_PASSWORD}@{MONGODB_SERVER_IP}:{MONGODB_PORT}"

utilsMain = KumikoEcoUtils()
utilsUser = KumikoEcoUserUtils()
userInvUtils = KumikoUserInvUtils()
today = datetime.utcnow()


class Marketplace(commands.Cog):
    """The general marketplace"""

    def __init__(self, bot):
        self.bot = bot

    eco_marketplace = SlashCommandGroup(
        name="eco-marketplace",
        description="Commands for Kumiko's Marketplace",
    )
    ecoMarketplaceUpdate = eco_marketplace.create_subgroup(
        name="update",
        description="Commands for updating items on the marketplace",
    )
    ecoMarketplaceDelete = eco_marketplace.create_subgroup(
        name="delete",
        description="Commands for deleting items on the marketplace",
    )
    ecoMarketplaceAdd = eco_marketplace.create_subgroup(
        "add", "Adds items into the marketplace"
    )

    @ecoMarketplaceAdd.command(name="item")
    @commands.cooldown(1, 43200, commands.BucketType.user)
    async def ecoAddItem(
        self,
        ctx,
    ):
        """Adds an item into the marketplace"""
        createItem = MarketplaceAddItem(
            mongo_uri=MARKETPLACE_CONNECTION_URI,
            postgres_uri=USERS_CONNECTION_URI,
            title="Add an item",
        )
        await ctx.send_modal(createItem)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    @eco_marketplace.command(name="view")
    async def ecoMarketplaceView(self, ctx):
        """View the marketplace"""
        try:
            mainObtain = await utilsMain.obtain(uri=MARKETPLACE_CONNECTION_URI)
            if len(mainObtain) == 0:
                raise NoItemsError
            else:
                paginator = pages.Paginator(
                    pages=[
                        discord.Embed(
                            title=dict(items)["name"],
                            description=dict(items)["description"],
                        )
                        .add_field(
                            name="Amount", value=dict(items)["amount"], inline=True
                        )
                        .add_field(
                            name="Price", value=dict(items)["price"], inline=True
                        )
                        .add_field(
                            name="Date Added",
                            value=parser.isoparse(dict(items)["date_added"]).strftime(
                                "%Y-%m-%d %H:%M:%S"
                            ),
                            inline=True,
                        )
                        .add_field(
                            name="Owner",
                            value=dict(items)["owner_name"],
                        )
                        for items in mainObtain
                    ],
                )
                await paginator.respond(ctx.interaction, ephemeral=False)
        except NoItemsError:
            embedErrorMain = discord.Embed()
            embedErrorMain.description = "There seems to be no items in the marketplace right now. Please try again..."
            await ctx.respond(embed=embedErrorMain)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    @eco_marketplace.command(
        name="search",
    )
    async def ecoMarketplaceSearch(
        self, ctx, *, name: Option(str, "The name of the item you wish to search")
    ):
        """Search the marketplace, and returns the first item found"""
        try:
            clientGetItem = motor.motor_asyncio.AsyncIOMotorClient(
                MARKETPLACE_CONNECTION_URI
            )
            await init_beanie(
                database=clientGetItem.kumiko_marketplace,
                document_models=[MarketplaceModel],
            )
            res = await MarketplaceModel.find(
                MarketplaceModel.name == name
            ).first_or_none()
            if res is None:
                raise NoItemsError
            else:
                embed = discord.Embed()
                embed.title = dict(res)["name"]
                embed.description = dict(res)["description"]
                embed.add_field(name="Amount", value=dict(res)["amount"])
                embed.add_field(name="Price", value=dict(res)["price"])
                embed.add_field(
                    name="Date Added",
                    value=parser.isoparse(dict(res)["date_added"]).strftime(
                        "%Y-%m-%d %H:%M:%S"
                    ),
                )
                embed.add_field(name="Owner", value=dict(res)["owner_name"])
                embed.add_field(name="Updated Price?", value=dict(res)["updated_price"])
                await ctx.respond(embed=embed)
        except NoItemsError:
            embedError = discord.Embed()
            embedError.description = (
                "Sorry, but the search produced no results. Please try again"
            )
            await ctx.respond(embed=embedError)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    @ecoMarketplaceDelete.command(name="all")
    async def ecoMarketplaceDeleteAll(self, ctx):
        """Deletes all of your items in the marketplace"""
        embed = discord.Embed()
        embed.description = "Do your really want to delete all of your items listed on the marketplace? There is no going back after this."
        await ctx.respond(
            embed=embed,
            view=MarketplacePurgeAllView(MARKETPLACE_CONNECTION_URI),
            ephemeral=True,
        )

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    @ecoMarketplaceDelete.command(name="one")
    async def ecoMarketplaceDeleteOne(self, ctx):
        """Deletes the specified item within the marketplace"""
        deleteModal = MarketplaceDeleteOneItem(
            mongo_uri=MARKETPLACE_CONNECTION_URI, title="Delete one item"
        )
        await ctx.send_modal(deleteModal)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    # TODO: Redo purchase command to use Modals instead
    @eco_marketplace.command(name="purchase")
    async def ecoMarketplacePurchase(
        self,
        ctx,
        *,
        item: Option(str, "The name of the item to purchase (case-sensitive)"),
        amount: Option(int, "The amount of items to purchase"),
        price: Option(int, "The price of the item. Note that you have to pay in full"),
    ):
        """Purchases an item from the marketplace"""
        try:
            beforePurchasing = await utilsMain.beforePurchase(
                owner_id=ctx.user.id, item_name=item, uri=MARKETPLACE_CONNECTION_URI
            )

            if len(beforePurchasing) == 0:
                raise NoItemsError
            else:
                for mainItems in beforePurchasing:
                    items = dict(mainItems)
                    checkIfUserHasItem = await userInvUtils.checkIfItemInUserInv(
                        user_id=ctx.author.id,
                        uuid=items["uuid"],
                        uri=USERS_CONNECTION_URI,
                    )
                    itemAuth = await utilsMain.purchaseAuth(
                        uuid=items["uuid"], uri=MARKETPLACE_CONNECTION_URI
                    )

                    for mainAuthItem in itemAuth:
                        auth = dict(mainAuthItem)

                        if auth["uuid"] == items["uuid"] and int(items["price"]) == int(
                            price
                        ):
                            if int(amount) > int(items["amount"]):
                                await ctx.respond(
                                    f"Sorry, but there is only {items['amount']} {items['name']} within the listing. You have requested more than that, so therefore the transaction is denied. Please try again."
                                )
                            elif int(amount) < int(items["amount"]):
                                if len(checkIfUserHasItem) == 0:
                                    totalAmountLeft = int(items["amount"]) - int(amount)
                                    await utilsMain.updateItemAmount(
                                        uuid=items["uuid"],
                                        amount=totalAmountLeft,
                                        uri=MARKETPLACE_CONNECTION_URI,
                                    )
                                    await userInvUtils.insertItem(
                                        user_uuid=str(uuid.uuid4()),
                                        user_id=ctx.author.id,
                                        date_acquired=datetime.utcnow().isoformat(),
                                        uuid=items["uuid"],
                                        name=items["name"],
                                        description=items["description"],
                                        amount=amount,
                                        uri=USERS_CONNECTION_URI,
                                    )
                                    await ctx.respond(
                                        f"Successfully purchased {amount} {items['name']} for {items['price']} coins."
                                    )
                                else:
                                    for userInvItem in checkIfUserHasItem:
                                        mainUserInvItem = dict(userInvItem)
                                        totalAmountRemaining = int(
                                            items["amount"]
                                        ) - int(amount)
                                        amountAddingToUser = (
                                            mainUserInvItem["amount"] + amount
                                        )
                                        await utilsMain.updateItemAmount(
                                            uuid=items["uuid"],
                                            amount=totalAmountRemaining,
                                            uri=MARKETPLACE_CONNECTION_URI,
                                        )
                                        await userInvUtils.updateItemAmount(
                                            user_id=ctx.user.id,
                                            uuid=items["uuid"],
                                            amount=amountAddingToUser,
                                            uri=USERS_CONNECTION_URI,
                                        )
                                        await ctx.respond(
                                            f"Successfully purchased {amount} {items['name']} for {items['price']} coins. You currently have {amountAddingToUser} {items['name']} in your inventory."
                                        )

                            elif int(amount) == int(items["amount"]):
                                if len(checkIfUserHasItem) == 0:
                                    await userInvUtils.insertItem(
                                        user_uuid=str(uuid.uuid4()),
                                        user_id=ctx.user.id,
                                        date_acquired=datetime.utcnow().isoformat(),
                                        uuid=items["uuid"],
                                        name=items["name"],
                                        description=items["description"],
                                        amount=amount,
                                        uri=USERS_CONNECTION_URI,
                                    )
                                    await utilsMain.updateItemAmount(
                                        uuid=items["uuid"],
                                        amount=int(amount)
                                        - int(
                                            items["amount"],
                                            uri=MARKETPLACE_CONNECTION_URI,
                                        ),
                                    )
                                    await ctx.respond(
                                        f"Successfully purchased {amount} {items['name']} for {items['price']} coins."
                                    )
                                else:
                                    for userInvItem3 in checkIfUserHasItem:
                                        mainUserInvItem = dict(userInvItem3)
                                        totalAmountRemaining = int(
                                            items["amount"]
                                        ) - int(amount)
                                        amountAddingToUser = (
                                            mainUserInvItem["amount"] + amount
                                        )
                                        await utilsMain.updateItemAmount(
                                            uuid=items["uuid"],
                                            amount=totalAmountRemaining,
                                            uri=MARKETPLACE_CONNECTION_URI,
                                        )
                                        await userInvUtils.updateItemAmount(
                                            user_id=ctx.user.id,
                                            uuid=items["uuid"],
                                            amount=amountAddingToUser,
                                            uri=USERS_CONNECTION_URI,
                                        )
                                        await ctx.respond(
                                            f"Successfully purchased {amount} {items['name']} for {items['price']} coins. You currently have {amountAddingToUser} {items['name']} in your inventory."
                                        )
                            else:
                                await ctx.respond(
                                    f'Unable to purchase {items["name"]} for {items["price"]} coins. Please try again'
                                )
                        else:
                            await ctx.respond(
                                f"Unable to purchase {items['name']} for {items['price']} coins. This is due to either the UUID's not matching up, or the incorrect price was given. Please try again"
                            )
        except NoItemsError:
            embedNoItemsError = discord.Embed()
            embedNoItemsError.description = "Sorry, but that item does not exist in the marketplace. Maybe try redoing your search? It is case sensitive so..."
            await ctx.respond(embed=embedNoItemsError)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    @ecoMarketplaceUpdate.command(name="amount")
    async def updateItemMarketplaceAmount(
        self,
        ctx,
    ):
        """Restocks your current item on the marketplace"""
        mainModal = MarketplaceUpdateAmount(
            mongo_uri=MARKETPLACE_CONNECTION_URI, title="Restock"
        )
        await ctx.send_modal(mainModal)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    @ecoMarketplaceUpdate.command(name="price")
    async def updateItemMarketplacePrice(self, ctx):
        """Updates the price of an item on the marketplace (Can only be used once)"""
        updateModal = MarketplaceUpdateItemPrice(
            mongo_uri=MARKETPLACE_CONNECTION_URI, title="Update Price"
        )
        await ctx.send_modal(updateModal)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


def setup(bot):
    bot.add_cog(Marketplace(bot))
