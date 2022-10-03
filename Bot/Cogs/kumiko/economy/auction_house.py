import asyncio
import os
import re
import uuid
from datetime import datetime

import aiormq
import discord
import uvloop
import yaml
from dateutil import parser
from discord.commands import Option, SlashCommandGroup
from discord.ext import commands, pages
from dotenv import load_dotenv
from economy_utils import KumikoAuctionHouseUtils, KumikoEcoUserUtils
from rin_exceptions import ItemNotFound, NoItemsError

load_dotenv()

RABBITMQ_USER = os.getenv("RabbitMQ_Username_Dev")
RABBITMQ_PASSWORD = os.getenv("RabbitMQ_Password_Dev")
REDIS_SERVER_IP = os.getenv("Redis_Server_IP_Dev")
REDIS_SERVER_PORT = os.getenv("Redis_Port_Dev")
RABBITMQ_SERVER_IP = os.getenv("RabbitMQ_Server_IP_Dev")
POSTGRES_PASSWORD = os.getenv("Postgres_Password_Dev")
POSTGRES_SERVER_IP = os.getenv("Postgres_Server_IP_Dev")
POSTGRES_USER_DATABASE = os.getenv("Postgres_Database_Dev")
POSTGRES_AH_DATABASE = os.getenv("Postgres_Database_AH_Dev")
POSTGRES_USERNAME = os.getenv("Postgres_Username_Dev")
CONNECTION_URI = f"postgresql+asyncpg://{POSTGRES_USERNAME}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER_IP}:5432/{POSTGRES_USER_DATABASE}"
AH_CONNECTION_URI = f"postgresql+asyncpg://{POSTGRES_USERNAME}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER_IP}:5432/{POSTGRES_AH_DATABASE}"

auctionHouseUtils = KumikoAuctionHouseUtils()
userUtils = KumikoEcoUserUtils()


class View(discord.ui.View):
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
        try:
            getUserInfo = await userUtils.selectUserRank(
                interaction.user.id, CONNECTION_URI
            )
            if len(getUserInfo) == 0:
                raise NoItemsError
            else:
                for items in getUserInfo:
                    if items < 25:
                        await interaction.response.send_message(
                            f"Sorry, but your current rank is {items}. You need at the very least rank 25 or higher to use this command."
                        )
                    else:
                        itemUUIDAuth = await auctionHouseUtils.obtainItemUUIDAuth(
                            user_id=interaction.user.id, uri=AH_CONNECTION_URI
                        )
                        try:
                            if len(itemUUIDAuth) == 0:
                                raise ItemNotFound
                            else:
                                await auctionHouseUtils.purgeUserAHItems(
                                    user_id=interaction.user.id, uri=AH_CONNECTION_URI
                                )
                                await interaction.response.send_message(
                                    "Confirmed. All Auction House Listings have now been completely purged from your account. This is permanent and irreversible."
                                )
                        except ItemNotFound:
                            await interaction.response.send_message(
                                "It seems like you don't have any to delete from at all..."
                            )
        except NoItemsError:
            await interaction.response.send_message(
                "It seems like you don't even have an account to begin with. Go ahead and create one first."
            )

    @discord.ui.button(
        label="No",
        row=0,
        style=discord.ButtonStyle.primary,
        emoji=discord.PartialEmoji.from_str("<:xmark:314349398824058880>"),
    )
    async def second_button_callback(self, button, interaction):
        await interaction.response.send_message("Well glad you choose not to...")


class AuctionHouse(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    auctionHouse = SlashCommandGroup(
        "eco-auction",
        "Auction off your highest items here",
        guild_ids=[970159505390325842],
    )
    auctionHouseDelete = auctionHouse.create_subgroup(
        "delete", "commands to delete stuff", guild_ids=[970159505390325842]
    )

    @auctionHouse.command(name="select")
    async def selectAHItem(
        self, ctx, *, name: Option(str, "The name of the item you wish to select")
    ):
        """Selects an item on the Auction House before to bid for"""
        try:
            getUserInfo = await userUtils.selectUserRank(ctx.author.id, CONNECTION_URI)
            if len(getUserInfo) == 0:
                raise ItemNotFound
            else:
                for items in getUserInfo:
                    if items < 25:
                        await ctx.respond(
                            f"Sorry, but your current rank is {items}. You need at the very least rank 25 in order to use this command."
                        )
                    else:
                        selectMainItem = await auctionHouseUtils.selectAHItemUUID(
                            name=name, uri=AH_CONNECTION_URI
                        )
                        for item in selectMainItem:
                            ahItemUUID = item
                        await auctionHouseUtils.setItemKey(
                            str(ctx.user.id),
                            ahItemUUID,
                            db=1,
                            ttl=21660,
                            redis_server_ip=REDIS_SERVER_IP,
                            redis_port=REDIS_SERVER_PORT,
                        )
                        await ctx.respond("Item selected")
        except ItemNotFound:
            await ctx.respond(
                "It seems like you don't even have an account to begin with. Go ahead and create one first."
            )

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    @auctionHouse.command(name="bid")
    async def bindForPrice(self, ctx, *, price: Option(int, "The price to bid")):
        """Bid for a higher price for an item"""
        try:
            try:
                getUserInfo = await userUtils.selectUserRank(
                    ctx.author.id, CONNECTION_URI
                )
                if len(getUserInfo) == 0:
                    raise ItemNotFound
                else:
                    for items in getUserInfo:
                        if items < 25:
                            await ctx.respond(
                                f"Sorry, but your current rank is {mainItems['rank']}. You need at the very least rank 25 in order to use this command."
                            )
                        else:
                            selectedItem = await auctionHouseUtils.getItemKey(
                                str(ctx.user.id),
                                db=1,
                                redis_server_ip=REDIS_SERVER_IP,
                                redis_port=REDIS_SERVER_PORT,
                            )
                            if selectedItem is None:
                                await ctx.respond(
                                    "You have not selected an item yet. Please run the command to select an item first."
                                )
                            else:
                                selectItemPriceRes = (
                                    await auctionHouseUtils.selectAHItemPrice(
                                        uuid=selectedItem, uri=AH_CONNECTION_URI
                                    )
                                )
                                for mainItems in selectItemPriceRes:
                                    selectItemPrice = mainItems
                                if price < int(selectItemPrice):
                                    raise ValueError
                                else:
                                    connection = await aiormq.connect(
                                        f"amqp://{RABBITMQ_USER}:{RABBITMQ_PASSWORD}@{RABBITMQ_SERVER_IP}/"
                                    )
                                    channel = await connection.channel()
                                    await channel.exchange_declare(
                                        exchange="auction_house", exchange_type="fanout"
                                    )
                                    body = bytes(f"{selectedItem}:{price}", "utf-8")
                                    await channel.basic_publish(
                                        body, exchange="auction_house"
                                    )
                                    await connection.close()
                                    await ctx.respond(f"bid placed ({price})")
            except ItemNotFound:
                await ctx.respond(
                    "It seems like you don't even have an account to begin with. Go ahead and create one first."
                )
        except ValueError:  # THIS NEEDS TO BE CHANGED OUT WITH A CUSTOM EXCEPTION LATER
            await ctx.respond(
                "It seems like the price given is lower than the one set. Please try again."
            )

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    @auctionHouse.command(name="add")
    async def addItemToAuctionHouse(
        self,
        ctx,
        *,
        name: Option(str, "The item that you are putting up for bidding"),
        description: Option(str, "The description of the item"),
        price: Option(int, "The initial price of the item"),
    ):
        """Adds an item to the Auction House"""
        dateAdded = datetime.now().isoformat()
        auctionHouseItemUUID = str(uuid.uuid4())
        userID = ctx.user.id
        filterFile = os.path.join(
            os.path.dirname(__file__), "config", "marketplace_filters.yml"
        )
        try:
            try:
                getUserInfo = await userUtils.obtainUserData(
                    ctx.author.id, CONNECTION_URI
                )
                if len(getUserInfo) == 0:
                    raise ItemNotFound
                else:
                    for items in getUserInfo:
                        mainItems = dict(items)
                    if mainItems["rank"] < 25:
                        await ctx.respond(
                            f"Sorry, but your current rank is {mainItems['rank']}. You need at the very least rank 25 in order to use this command."
                        )
                    elif mainItems["rank"] > 25 and mainItems["lavender_petals"] < 1500:
                        await ctx.respond(
                            "It seems like you don't have enough money to list. You need at the very least 1500 Petals to list"
                        )
                    elif (
                        mainItems["rank"] > 25 and mainItems["lavender_petals"] >= 1500
                    ):
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
                                await auctionHouseUtils.addAuctionHouseItem(
                                    auctionHouseItemUUID,
                                    userID,
                                    filteredItemName,
                                    filteredItemDescription,
                                    dateAdded,
                                    price,
                                    False,
                                    AH_CONNECTION_URI,
                                )
                                await auctionHouseUtils.setItemKey(
                                    auctionHouseItemUUID,
                                    price,
                                    db=0,
                                    ttl=86400,
                                    redis_server_ip=REDIS_SERVER_IP,
                                    redis_port=REDIS_SERVER_PORT,
                                )
                                await ctx.respond("Item added to the auction house")
                            except yaml.YAMLError:
                                await ctx.respond(
                                    "Oops, something went wrong with the yaml file! Please try again."
                                )

            except ItemNotFound:
                await ctx.respond(
                    "It seems like you don't even have an account to begin with. Go ahead and create one first."
                )
        except Exception:
            await ctx.respond(
                embed=discord.Embed(
                    description="Oops, something went wrong! Please try again."
                )
            )

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    @auctionHouse.command(name="view")
    async def viewAHItems(self, ctx):
        """Views all of the items on the AH for bidding"""
        try:
            getUserInfo = await userUtils.selectUserRank(ctx.author.id, CONNECTION_URI)
            if len(getUserInfo) == 0:
                raise NoItemsError
            else:
                for items in getUserInfo:
                    if items < 25:
                        await ctx.respond(
                            f"Sorry, but your current rank is {items}. You need at the very least rank 25 or higher to use this command."
                        )
                    else:
                        mainRes = await auctionHouseUtils.selectItemNotPassed(
                            False, AH_CONNECTION_URI
                        )
                        try:
                            if len(mainRes) == 0:
                                raise ItemNotFound
                            else:
                                mainPages = pages.Paginator(
                                    pages=[
                                        discord.Embed(
                                            title=dict(items)["name"],
                                            description=dict(items)["description"],
                                        )
                                        .add_field(
                                            name="Date Added",
                                            value=parser.isoparse(
                                                dict(items)["date_added"]
                                            ).strftime("%Y-%m-%d %H:%M:%S"),
                                            inline=True,
                                        )
                                        .add_field(
                                            name="Price",
                                            value=dict(items)["price"],
                                            inline=True,
                                        )
                                        for items in mainRes
                                    ],
                                    loop_pages=True,
                                )
                                await mainPages.respond(
                                    ctx.interaction, ephemeral=False
                                )
                        except ItemNotFound:
                            embedError = discord.Embed()
                            embedError.description = "There are no items to be seen on the Auction House. Come back later for more!"
                            await ctx.respond(embed=embedError)
        except NoItemsError:
            await ctx.respond(
                "It seems like you don't even have an account to begin with. Go ahead and create one first."
            )

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    @auctionHouseDelete.command(name="one")
    async def userDelOne(
        self, ctx, *, name: Option(str, "The name of the item to delete")
    ):
        """Deletes one user from the user for the Auction House"""
        try:
            getUserInfo = await userUtils.selectUserRank(ctx.author.id, CONNECTION_URI)
            if len(getUserInfo) == 0:
                raise NoItemsError
            else:
                for items in getUserInfo:
                    if items < 25:
                        await ctx.respond(
                            f"Sorry, but your current rank is {items}. You need at the very least rank 25 or higher to use this command."
                        )
                    else:
                        userSelRes = await auctionHouseUtils.selectUserItemViaName(
                            ctx.author.id, name, AH_CONNECTION_URI
                        )
                        try:
                            if len(userSelRes) == 0:
                                raise ItemNotFound
                            else:
                                for items in userSelRes:
                                    mainItems = dict(items)
                                    itemUUID = mainItems["uuid"]
                                    await auctionHouseUtils.deleteUserAHItem(
                                        ctx.author.id, itemUUID, AH_CONNECTION_URI
                                    )
                                await ctx.respond("Item deleted")
                        except ItemNotFound:
                            embedError = discord.Embed()
                            embedError.description = f"There are no items within the Auction House that has the name of {name}. Please try again."
                            await ctx.respond(embed=embedError)
        except NoItemsError:
            await ctx.respond(
                "It seems like you don't even have an account to begin with. Go ahead and create one first."
            )

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    @auctionHouseDelete.command(name="all")
    async def purgeUserAHItems(self, ctx):
        """Purges all of the user's listed Auction House items. This cannot be recovered from"""
        embed = discord.Embed()
        embed.description = "Are you sure you want to purge all of your Auction House listings? This is permanent and cannot be undone."
        await ctx.respond(embed=embed, view=View())

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


def setup(bot):
    bot.add_cog(AuctionHouse(bot))
