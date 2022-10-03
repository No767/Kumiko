import asyncio
import os
import re
import uuid
from datetime import datetime

import discord
import uvloop
import yaml
from dateutil import parser
from discord.commands import Option, SlashCommandGroup
from discord.ext import commands, pages
from dotenv import load_dotenv
from economy_utils import (KumikoEcoUserUtils, KumikoEcoUtils,
                           KumikoUserInvUtils)
from rin_exceptions import ItemNotFound, NoItemsError

load_dotenv()

POSTGRES_PASSWORD = os.getenv("Postgres_Password_Dev")
POSTGRES_SERVER_IP = os.getenv("Postgres_Server_IP_Dev")
POSTGRES_DATABASE = os.getenv("Postgres_Database_Dev")
POSTGRES_USERNAME = os.getenv("Postgres_Username_Dev")
POSTGRES_SERVER_PORT = os.getenv("Postgres_Port_Dev")
MONGODB_PASSWORD = os.getenv("MongoDB_Password_Dev")
MONGODB_USERNAME = os.getenv("MongoDB_Username_Dev")
MONGODB_SERVER_IP = os.getenv("MongoDB_Server_IP_Dev")
MONGODB_PORT = os.getenv("MongoDB_Server_Port_Dev")

USERS_CONNECTION_URI = f"postgresql+asyncpg://{POSTGRES_USERNAME}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER_IP}:5432/{POSTGRES_DATABASE}"
MARKETPLACE_CONNECTION_URI = f"mongodb://{MONGODB_USERNAME}:{MONGODB_PASSWORD}@{MONGODB_SERVER_IP}:{MONGODB_PORT}"

utilsMain = KumikoEcoUtils()
utilsUser = KumikoEcoUserUtils()
userInvUtils = KumikoUserInvUtils()
today = datetime.utcnow()


class PurgeAllView(discord.ui.View):
    async def on_timeout(self):
        for child in self.children:
            child.disabled = True

    @discord.ui.button(
        label="Yes",
        row=0,
        style=discord.ButtonStyle.primary,
        emoji=discord.PartialEmoji.from_str("<:check:314349398811475968>"),
    )
    async def button_callback(self, button, interaction):
        mainChecker = await utilsMain.getAllOwnersItems(
            owner=interaction.user.id, uri=MARKETPLACE_CONNECTION_URI
        )
        try:
            if len(mainChecker) == 0:
                raise NoItemsError
            else:
                for items in mainChecker:
                    await utilsMain.purgeOwnersItems(
                        uuid=dict(items)["uuid"],
                        owner=dict(items)["owner"],
                        uri=MARKETPLACE_CONNECTION_URI,
                    )
                await interaction.response.send_message(
                    "All of your items listed on the marketplace have been deleted",
                    ephemeral=True,
                )
        except NoItemsError:
            await interaction.response.send_message(
                "You don't have any items listed on the marketplace to delete. The transaction has been cancelled.",
                ephemeral=True,
            )

    @discord.ui.button(
        label="No",
        row=0,
        style=discord.ButtonStyle.primary,
        emoji=discord.PartialEmoji.from_str("<:xmark:314349398824058880>"),
    )
    async def second_button_callback(self, button, interaction):
        await interaction.response.send_message(
            "Welp, you choose not to ig...", ephemeral=True
        )


class Marketplace(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    eco_marketplace = SlashCommandGroup(
        name="eco-marketplace",
        description="Commands for Kumiko's Marketplace",
    )
    ecoMarketplaceUpdate = eco_marketplace.create_subgroup(
        name="update",
        description="Commands for updating items on the marketplace",
        guild_ids=[970159505390325842],
    )
    ecoMarketplaceDelete = eco_marketplace.create_subgroup(
        name="delete",
        description="Commands for deleting items on the marketplace",
        guild_ids=[970159505390325842],
    )
    ecoMarketplaceAdd = eco_marketplace.create_subgroup(
        "add", "Adds items into the marketplace", guild_ids=[970159505390325842]
    )

    @ecoMarketplaceAdd.command(name="item")
    @commands.cooldown(1, 43200, commands.BucketType.user)
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
        dateEntry = today.isoformat()
        owner = ctx.user.id
        uuidItem = uuid.uuid4().hex[:16]
        filterFile = os.path.join(
            os.path.dirname(__file__), "config", "marketplace_filters.yml"
        )
        try:
            try:
                getUserData = await utilsUser.obtainUserData(
                    ctx.user.id, USERS_CONNECTION_URI
                )
                if len(getUserData) == 0:
                    raise ItemNotFound
                else:
                    for item in getUserData:
                        mainItem = dict(item)
                    finalBal = int(mainItem["lavender_petals"]) - 10
                    await utilsUser.updateUserLavenderPetals(
                        user_id=ctx.user.id,
                        lavender_petals=finalBal,
                        uri=USERS_CONNECTION_URI,
                    )
                    with open(filterFile, "r") as stream:
                        try:
                            filterList = yaml.safe_load(stream)
                            mainFilterList = filterList["filters"]
                            mainFilter = re.compile(
                                "|".join([str(item) for item in mainFilterList]),
                                re.IGNORECASE,
                            )
                            filteredItemName = re.sub(mainFilter, "item", str(name))
                            filteredItemDescription = re.sub(
                                mainFilter, "item", str(description)
                            )
                            await utilsMain.ins(
                                uuidItem,
                                dateEntry,
                                owner,
                                MARKETPLACE_CONNECTION_URI,
                                filteredItemName,
                                filteredItemDescription,
                                amount,
                                price,
                                updatedPrice=False,
                            )
                            await ctx.respond("Item added to the marketplace")
                        except yaml.YAMLError:
                            await ctx.respond(
                                "Oops, something went wrong with the yaml file! Please try again."
                            )
            except ItemNotFound:
                embedError = discord.Embed()
                embedError.description = "It seems like that your account was not found. Please initialize your account first."
                await ctx.respond(embed=embedError)
        except Exception:
            await ctx.respond(
                embed=discord.Embed(
                    description="Oops, something went wrong! Please try again."
                )
            )

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
                            value=f"{await self.bot.fetch_user(dict(items)['owner'])}",
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
        """Search the marketplace"""
        try:
            mainGetItem = await utilsMain.getItem(
                name=name, uri=MARKETPLACE_CONNECTION_URI
            )
            if len(mainGetItem) == 0:
                raise NoItemsError
            else:
                paginator = pages.Paginator(
                    pages=[
                        discord.Embed(
                            title=dict(item)["name"],
                            description=dict(item)["description"],
                        )
                        .add_field(
                            name="Amount", value=dict(item)["amount"], inline=True
                        )
                        .add_field(name="Price", value=dict(item)["price"], inline=True)
                        .add_field(
                            name="Date Added",
                            value=parser.isoparse(dict(item)["date_added"]).strftime(
                                "%Y-%m-%d %H:%M:%S"
                            ),
                            inline=True,
                        )
                        .add_field(
                            name="Owner",
                            value=f"{await self.bot.fetch_user(dict(item)['owner'])}",
                        )
                        for item in mainGetItem
                    ]
                )
                await paginator.respond(ctx.interaction, ephemeral=False)
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
        await ctx.respond(embed=embed, view=PurgeAllView())

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    @ecoMarketplaceDelete.command(name="one")
    async def ecoMarketplaceDeleteOne(
        self, ctx, *, name: Option(str, "The name of the item")
    ):
        """Deletes the specified item within the marketplace"""
        try:
            mainChecker = await utilsMain.getItemUUIDWithName(
                name=name, owner=ctx.user.id, uri=MARKETPLACE_CONNECTION_URI
            )
            if len(mainChecker) == 0:
                raise NoItemsError
            else:
                for items in mainChecker:
                    await utilsMain.delItemUUID(
                        uuid=dict(items)["uuid"], uri=MARKETPLACE_CONNECTION_URI
                    )
                await ctx.respond("Item deleted from the marketplace")
        except NoItemsError:
            await ctx.respond("Sorry, but that item does not exist in the marketplace.")

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

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
        *,
        name: Option(str, "The name of the item"),
        amount: Option(int, "The new amount of items you wish to restock with"),
    ):
        """Restocks your current item on the marketplace"""
        mainRes = await utilsMain.getUserItem(
            name=name, user_id=ctx.user.id, uri=MARKETPLACE_CONNECTION_URI
        )
        try:
            if len(mainRes) == 0:
                raise ItemNotFound
            else:
                for item in mainRes:
                    mainItem = dict(item)
                    await utilsMain.updateItemAmount(
                        uuid=mainItem["uuid"],
                        amount=mainItem["amount"] + amount,
                        uri=MARKETPLACE_CONNECTION_URI,
                    )
                    await ctx.respond(
                        f'Successfully updated {mainItem["name"]} to {mainItem["amount"] + amount}'
                    )
        except ItemNotFound:
            embedError = discord.Embed()
            embedError.description = "Sorry, it seems like the item you are trying to update does not exist in the Marketplace. Please try again."
            await ctx.respond(embed=embedError)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    @ecoMarketplaceUpdate.command(name="price")
    async def updateItemMarketplacePrice(
        self,
        ctx,
        *,
        name: Option(str, "The name of the item to update"),
        price: Option(int, "The new price you wish to set"),
    ):
        """Updates the price of an item on the marketplace (Can only be used once)"""
        mainRes = await utilsMain.getUserItem(
            name=name, user_id=ctx.user.id, uri=MARKETPLACE_CONNECTION_URI
        )
        try:
            if len(mainRes) == 0:
                raise ItemNotFound
            else:
                for item in mainRes:
                    mainDictItem = dict(item)
                    if mainDictItem["updated_price"] is False:
                        await utilsMain.updateItemPrice(
                            user_id=ctx.user.id,
                            uuid=mainDictItem["uuid"],
                            price=price,
                            updated_price=True,
                            uri=MARKETPLACE_CONNECTION_URI,
                        )
                        await ctx.respond(
                            f"Successfully updated the price of the item {name}."
                        )
                    else:
                        await ctx.respond(
                            "Sadly you can't update the price of the item. You can only update it once."
                        )
        except ItemNotFound:
            embedError = discord.Embed()
            embedError.description = "Sorry, it seems like the item you are trying to update does not exist in the Marketplace. Please try again."
            await ctx.respond(embed=embedError)


def setup(bot):
    bot.add_cog(Marketplace(bot))
