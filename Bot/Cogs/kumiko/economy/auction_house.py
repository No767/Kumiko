import asyncio
import os

import discord
import uvloop
from dateutil import parser
from discord.commands import Option, SlashCommandGroup
from discord.ext import commands, pages
from dotenv import load_dotenv
from economy_utils import KumikoAuctionHouseUtils, KumikoEcoUserUtils
from kumiko_ui_components import AHCreateItemModal, AHDeleteItemModal, AHPurgeAllView
from rin_exceptions import ItemNotFound, NoItemsError

load_dotenv()

REDIS_SERVER_IP = os.getenv("Redis_Server_IP")
REDIS_SERVER_PORT = os.getenv("Redis_Port")
POSTGRES_PASSWORD = os.getenv("Postgres_Password")
POSTGRES_SERVER_IP = os.getenv("Postgres_Server_IP")
POSTGRES_DB = os.getenv("Postgres_Kumiko_Database")
POSTGRES_USERNAME = os.getenv("Postgres_Username")
POSTGRES_PORT = os.getenv("Postgres_Port")
CONNECTION_URI = f"postgresql+asyncpg://{POSTGRES_USERNAME}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER_IP}:{POSTGRES_PORT}/{POSTGRES_DB}"
AH_CONNECTION_URI = f"postgresql+asyncpg://{POSTGRES_USERNAME}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER_IP}:{POSTGRES_PORT}/{POSTGRES_DB}"

auctionHouseUtils = KumikoAuctionHouseUtils()
userUtils = KumikoEcoUserUtils()


class AuctionHouse(commands.Cog):
    """A place reserved for the elites for auctioning high value items"""

    def __init__(self, bot):
        self.bot = bot

    auctionHouse = SlashCommandGroup(
        "eco-auction",
        "Auction off your highest items here",
    )
    auctionHouseDelete = auctionHouse.create_subgroup(
        "delete", "commands to delete stuff"
    )

    @auctionHouse.command(name="select")
    async def selectAHItem(
        self, ctx, *, name: Option(str, "The name of the item you wish to select")
    ):
        """Selects an item on the Auction House before to bid for"""
        try:
            getUserInfo = await userUtils.getFirstUser(
                user_id=ctx.author.id, uri=CONNECTION_URI
            )
            if getUserInfo is None:
                raise ItemNotFound
            else:
                if dict(getUserInfo)["rank"] < 25:
                    await ctx.respond(
                        f"Sorry, but your current rank is {dict(getUserInfo)['rank']}. You need at the very least rank 25 in order to use this command."
                    )
                else:
                    selectMainItem = await auctionHouseUtils.selectFirstItem(
                        name=name, uri=AH_CONNECTION_URI
                    )
                    if selectMainItem is None:
                        await ctx.respond(
                            "It seems like the item requested could not be found. Please try again later"
                        )
                    else:
                        await auctionHouseUtils.setItemKey(
                            key=str(ctx.user.id),
                            value=dict(selectMainItem)["uuid"],
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
            getUserInfo = await userUtils.getFirstUser(
                user_id=ctx.author.id, uri=CONNECTION_URI
            )
            if getUserInfo is None:
                raise ItemNotFound
            else:
                if dict(getUserInfo)["rank"] < 25:
                    await ctx.respond(
                        f"Sorry, but your current rank is {dict(getUserInfo)['rank']}. You need at the very least rank 25 in order to use this command."
                    )
                else:
                    selectedItem = await auctionHouseUtils.getItemKey(
                        key=str(ctx.user.id),
                        db=1,
                        redis_server_ip=REDIS_SERVER_IP,
                        redis_port=REDIS_SERVER_PORT,
                    )
                    if selectedItem is None:
                        await ctx.respond(
                            "You have not selected an item yet. Please run the command to select an item first."
                        )
                    else:
                        getSelectedItem = (
                            await auctionHouseUtils.selectFirstItemViaUUID(
                                uuid=selectedItem, uri=AH_CONNECTION_URI
                            )
                        )
                        try:
                            if price < int(dict(getSelectedItem)["price"]):
                                raise ValueError
                            else:
                                await auctionHouseUtils.setItemKey(
                                    key=f"{ctx.user.id}-{selectedItem}-bid",
                                    value=price,
                                    db=1,
                                    ttl=3600,
                                    redis_server_ip=REDIS_SERVER_IP,
                                    redis_port=REDIS_SERVER_PORT,
                                )
                                await ctx.respond(f"Bid set for {price}")
                        except ValueError:
                            await ctx.respond(
                                "It seems like the price given is lower than the one set. Please try again."
                            )
        except ItemNotFound:
            await ctx.respond(
                "It seems like you don't even have an account to begin with. Go ahead and create one first."
            )

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    @auctionHouse.command(name="add")
    async def addItemToAuctionHouse(
        self,
        ctx,
    ):
        """Adds an item to the Auction House"""
        mainModal = AHCreateItemModal(
            uri=AH_CONNECTION_URI,
            redis_host=REDIS_SERVER_IP,
            redis_port=REDIS_SERVER_PORT,
            title="Create an item",
        )
        await ctx.send_modal(mainModal)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    @auctionHouse.command(name="view")
    async def viewAHItems(self, ctx):
        """Views all of the items on the AH for bidding"""
        try:
            getUserInfo = await userUtils.getFirstUser(
                user_id=ctx.author.id, uri=CONNECTION_URI
            )
            if getUserInfo is None:
                raise NoItemsError
            else:
                if dict(getUserInfo)["rank"] < 25:
                    await ctx.respond(
                        f"Sorry, but your current rank is {dict(getUserInfo)['rank']}. You need at the very least rank 25 or higher to use this command."
                    )
                else:
                    mainRes = await auctionHouseUtils.selectItemNotPassed(
                        passed=False, uri=AH_CONNECTION_URI
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
                            await mainPages.respond(ctx.interaction, ephemeral=False)
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
    async def userDelOne(self, ctx):
        """Deletes one user from the user for the Auction House"""
        mainModal = AHDeleteItemModal(uri=AH_CONNECTION_URI, title="Delete an item")
        await ctx.send_modal(mainModal)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    @auctionHouseDelete.command(name="all")
    async def purgeUserAHItems(self, ctx):
        """Purges all of the user's listed Auction House items. This cannot be recovered from"""
        embed = discord.Embed()
        embed.description = "Are you sure you want to purge all of your Auction House listings? This is permanent and cannot be undone."
        await ctx.respond(
            embed=embed, view=AHPurgeAllView(uri=AH_CONNECTION_URI), ephemeral=True
        )

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


def setup(bot):
    bot.add_cog(AuctionHouse(bot))
