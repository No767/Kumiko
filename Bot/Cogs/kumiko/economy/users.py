import asyncio
import os
import urllib.parse
from typing import List

import discord
import uvloop
from dateutil import parser
from discord.commands import SlashCommandGroup
from discord.ext import commands, pages
from dotenv import load_dotenv
from kumiko_economy import EcoUserBridge
from kumiko_economy_utils import KumikoEcoUserUtils, KumikoUserInvUtils
from kumiko_ui_components import CreateAccountView, PurgeAccountView
from kumiko_utils import KumikoCM
from rin_exceptions import ItemNotFound, NoItemsError

load_dotenv()

POSTGRES_PASSWORD = urllib.parse.quote_plus(os.getenv("Postgres_Password"))
POSTGRES_SERVER_IP = os.getenv("Postgres_Server_IP")
POSTGRES_WS_DATABASE = os.getenv("Postgres_Kumiko_Database")
POSTGRES_USERNAME = os.getenv("Postgres_Username")
POSTGRES_PORT = os.getenv("Postgres_Port")
CONNECTION_URI = f"asyncpg://{POSTGRES_USERNAME}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER_IP}:{POSTGRES_PORT}/{POSTGRES_WS_DATABASE}"
MODELS = ["kumiko_economy.models"]

# Old values
# POSTGRES_PASSWORD = os.getenv("Postgres_Password")
# POSTGRES_SERVER_IP = os.getenv("Postgres_Server_IP")
# POSTGRES_DATABASE = os.getenv("Postgres_Kumiko_Database")
# POSTGRES_USERNAME = os.getenv("Postgres_Username")
# POSTGRES_PORT = os.getenv("Postgres_Port")
# CONNECTION_URI = f"postgresql+asyncpg://{POSTGRES_USERNAME}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER_IP}:{POSTGRES_PORT}/{POSTGRES_DATABASE}"

utilsUser = KumikoEcoUserUtils()
inv = KumikoUserInvUtils()


class EcoUsers(commands.Cog):
    """Commands for checking user's accounts and balances"""

    def __init__(self, bot):
        self.bot = bot

    eco_users = SlashCommandGroup(
        name="eco-users",
        description="Commands for handling user-related data and transactions for Kumiko's economy system",
    )
    ecoUsersDelete = eco_users.create_subgroup("delete", "Delete user data")

    @eco_users.command(name="init")
    async def ecoInit(self, ctx):
        """Initialize your user account"""
        embed = discord.Embed()
        embed.description = "Do you wish to initialize your economy account? This is completely optional. Click on the buttons to confirm"
        await ctx.respond(
            embed=embed, view=CreateAccountView(CONNECTION_URI), ephemeral=True
        )

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    @eco_users.command(name="balance")
    async def ecoBal(self, ctx):
        """Gets your user balance profile"""
        mainProfile = await utilsUser.getFirstUser(
            user_id=ctx.user.id, uri=CONNECTION_URI
        )
        try:
            if mainProfile is None:
                raise ItemNotFound
            else:
                embed = discord.Embed()
                embed.title = f"{ctx.user.name}'s Balance"
                embed.add_field(
                    name="Petals", value=dict(mainProfile)["lavender_petals"]
                )
                embed.set_thumbnail(url=ctx.user.display_avatar.url)
                await ctx.respond(embed=embed, ephemeral=True)
        except ItemNotFound:
            embedError = discord.Embed()
            embedError.description = "It seems like that your account was not found. Please initialize your account first."
            await ctx.respond(embed=embedError, ephemeral=True)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    @eco_users.command(name="profile")
    async def ecoProfile(self, ctx):
        """Gets your user economy profile"""
        mainProfile = await utilsUser.getFirstUser(
            user_id=ctx.user.id, uri=CONNECTION_URI
        )
        try:
            if mainProfile is None:
                raise ItemNotFound
            else:
                embed = discord.Embed()
                embed.title = f"{dict(mainProfile)['username']}'s Profile"
                embed.add_field(
                    name="Petals", value=dict(mainProfile)["lavender_petals"]
                )
                embed.add_field(name="Rank", value=dict(mainProfile)["rank"])
                embed.add_field(
                    name="Date Joined",
                    value=parser.isoparse(dict(mainProfile)["date_joined"]).strftime(
                        "%Y-%m-%d %H:%M:%S"
                    ),
                )
                embed.set_thumbnail(url=ctx.user.display_avatar.url)
                await ctx.respond(embed=embed, ephemeral=True)
        except ItemNotFound:
            embedError = discord.Embed()
            embedError.description = "It seems like that your account was not found. Please initialize your account first."
            await ctx.respond(embed=embedError, ephemeral=True)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    @eco_users.command(name="improved-profile")
    async def improvedProfile(self, ctx: discord.ApplicationContext):
        """An improved version of the profile cmd"""
        # The caching will be added later
        async with KumikoCM(uri=CONNECTION_URI, models=MODELS):
            try:
                userData = await EcoUserBridge.get_or_none(
                    user_bridge_id=454357482102587393
                ).prefetch_related("user_inv")
                if userData is None:
                    raise ItemNotFound
                else:
                    # Should all be cached later
                    userInv = await userData.user_inv.all().values()
                    userQuests = await userData.quests.all().values()
                    userMarketplace = await userData.marketplace.all().values()
                    userAuctionHouse = await userData.auction_house.all().values()
                    pageGroups = [
                        pages.PageGroup(
                            pages=[
                                discord.Embed(description=item["name"])
                                for item in await userData.user_inv.all().values()
                            ]
                            if isinstance(userInv, List)
                            else [discord.Embed(description=userInv["name"])],
                            label="Inventory",
                            description="user inv",
                        ),
                        pages.PageGroup(
                            pages=[
                                discord.Embed(description=item["name"])
                                for item in userQuests
                            ]
                            if isinstance(userQuests, List)
                            else [discord.Embed(description=userQuests["name"])],
                            label="Quests",
                            description="user quests",
                        ),
                        pages.PageGroup(
                            pages=[
                                discord.Embed(description=item["name"])
                                for item in userMarketplace
                            ]
                            if isinstance(userMarketplace, List)
                            else [discord.Embed(description=userMarketplace["name"])],
                            label="Marketplace",
                            description="user marketplace",
                        ),
                        pages.PageGroup(
                            pages=[
                                discord.Embed(description=item["name"])
                                for item in userAuctionHouse
                            ]
                            if isinstance(userAuctionHouse, List)
                            else [discord.Embed(description=userAuctionHouse["name"])],
                            label="Auction House",
                            description="user auction house",
                        ),
                    ]
                    mainPages = pages.Paginator(
                        pages=pageGroups, show_menu=True, loop_pages=True
                    )
                    await mainPages.respond(ctx.interaction, ephemeral=True)
            except ItemNotFound:
                embedError = discord.Embed()
                embedError.description = "It seems like that your account was not found. Please initialize your account first."
                return await ctx.respond(embed=embedError, ephemeral=True)

    @eco_users.command(name="inv")
    async def ecoUserInv(self, ctx):
        """Access your inventory"""
        try:
            userInv = await inv.getUserInv(user_id=ctx.user.id, uri=CONNECTION_URI)
            if len(userInv) == 0:
                raise NoItemsError
            else:
                mainPages = pages.Paginator(
                    pages=[
                        discord.Embed(
                            title=dict(items)["name"],
                            description=dict(items)["description"],
                        )
                        .add_field(
                            name="Date First Acquired",
                            value=parser.isoparse(
                                dict(items)["date_acquired"]
                            ).strftime("%Y-%m-%d %H:%M:%S"),
                            inline=True,
                        )
                        .add_field(
                            name="Amount", value=dict(items)["amount"], inline=True
                        )
                        for items in userInv
                    ],
                    loop_pages=True,
                )
                await mainPages.respond(ctx.interaction, ephemeral=True)
        except NoItemsError:
            embedTypeError = discord.Embed()
            embedTypeError.description = "It seems you don't have any items in your inventory! Start purchasing some items from the marketplace to get started!"
            await ctx.respond(embed=embedTypeError, ephemeral=True)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    @ecoUsersDelete.command(name="account")
    async def purgeUserAcct(self, ctx):
        """Permanently deletes your user eco account"""
        embed = discord.Embed()
        embed.description = "Do you really want to delete your eco account? This is a permanent action and cannot be undone. Click on the buttons to confirm"
        await ctx.respond(
            embed=embed, view=PurgeAccountView(CONNECTION_URI), ephemeral=True
        )


def setup(bot):
    bot.add_cog(EcoUsers(bot))
