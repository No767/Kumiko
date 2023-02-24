import asyncio
import os
import urllib.parse

import discord
import uvloop
from discord.commands import SlashCommandGroup
from discord.ext import commands, pages
from discord.utils import format_dt
from dotenv import load_dotenv
from kumiko_economy import KumikoEconomyCacheUtils
from kumiko_ui_components import EcoUserCreationView, EcoUserPurgeView
from kumiko_utils import parseDatetime
from rin_exceptions import ItemNotFound, NoItemsError

load_dotenv()

REDIS_HOST = os.getenv("Redis_Server_IP")
REDIS_PORT = os.getenv("Redis_Port")
POSTGRES_PASSWORD = urllib.parse.quote_plus(os.getenv("Postgres_Password"))
POSTGRES_SERVER_IP = os.getenv("Postgres_Server_IP")
POSTGRES_WS_DATABASE = os.getenv("Postgres_Kumiko_Database")
POSTGRES_USERNAME = os.getenv("Postgres_Username")
POSTGRES_PORT = os.getenv("Postgres_Port")
CONNECTION_URI = f"asyncpg://{POSTGRES_USERNAME}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER_IP}:{POSTGRES_PORT}/{POSTGRES_WS_DATABASE}"
MODELS = ["kumiko_economy.models"]

cache = KumikoEconomyCacheUtils(
    uri=CONNECTION_URI, models=MODELS, redis_host=REDIS_HOST, redis_port=REDIS_PORT
)


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
        await ctx.respond(embed=embed, view=EcoUserCreationView(), ephemeral=True)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    @eco_users.command(name="balance")
    async def ecoBal(self, ctx):
        """Gets your user balance profile"""
        userData = await cache.cacheUser(
            user_id=ctx.user.id, command_name=ctx.command.qualified_name
        )
        try:
            if userData is None:
                raise ItemNotFound
            else:
                embed = discord.Embed()
                embed.title = f"{userData['username']}'s Balance"
                embed.description = f'**Petals**: {userData["lavender_petals"]}'
                embed.set_thumbnail(url=ctx.user.display_avatar.url)
                await ctx.respond(embed=embed, ephemeral=True)
        except ItemNotFound:
            embedError = discord.Embed()
            embedError.description = "It seems like that your account was not found. Please initialize your account first."
            await ctx.respond(embed=embedError, ephemeral=True)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    @eco_users.command(name="profile")
    async def improvedProfile(self, ctx: discord.ApplicationContext):
        """View your user economy profile"""
        try:
            userData = await cache.cacheUser(
                user_id=ctx.user.id, command_name=ctx.command.qualified_name
            )
            if userData is None:
                raise ItemNotFound
            else:
                pageGroups = [
                    pages.PageGroup(
                        pages=[
                            discord.Embed(title=userData["username"])
                            .add_field(
                                name="Lavender Petals",
                                value=userData["lavender_petals"],
                            )
                            .add_field(name="Rank", value=userData["rank"])
                            .add_field(
                                name="Date Joined",
                                value=format_dt(parseDatetime(userData["date_joined"])),
                            )
                            .set_thumbnail(url=ctx.user.display_avatar.url)
                        ],
                        label="User Profile",
                        description="View your general profile here",
                    ),
                    pages.PageGroup(
                        pages=[
                            discord.Embed(
                                title=items["name"], description=items["description"]
                            )
                            .add_field(name="Amount", value=items["amount"])
                            .add_field(
                                name="Date Acquired",
                                value=format_dt(parseDatetime(items["date_acquired"])),
                            )
                            for items in userData["user_inv"]
                        ],
                        label="User Inv",
                        description="View your inventory",
                    ),
                    pages.PageGroup(
                        pages=[
                            discord.Embed(
                                title=marketplaceItems["name"],
                                description=marketplaceItems["description"],
                            )
                            .add_field(name="Price", value=marketplaceItems["price"])
                            .add_field(name="Amount", value=marketplaceItems["amount"])
                            .add_field(
                                name="Date Added",
                                value=format_dt(
                                    parseDatetime(marketplaceItems["date_added"])
                                ),
                            )
                            for marketplaceItems in userData["marketplace"]
                        ],
                        label="Marketplace",
                        description="View the items you are selling at the Marketplace",
                    ),
                    pages.PageGroup(
                        pages=[
                            discord.Embed(
                                title=quests["name"], description=quests["description"]
                            )
                            .add_field(
                                name="End Date",
                                value=format_dt(parseDatetime(quests["end_datetime"])),
                            )
                            .add_field(
                                name="Date Created",
                                value=format_dt(parseDatetime(quests["date_created"])),
                            )
                            .add_field(name="Reward", value=quests["reward"])
                            .add_field(name="Active", value=quests["active"])
                            .add_field(name="Claimed", value=quests["claimed"])
                            for quests in userData["quests"]
                        ],
                        label="Quests",
                        description="View all of your created quests",
                    ),
                ]
                if userData["rank"] >= 25:
                    pageGroups.append(
                        pages.PageGroup(
                            pages=[
                                discord.Embed(
                                    title=ahItems["name"],
                                    description=ahItems["description"],
                                )
                                .add_field(name="Price", value=ahItems["price"])
                                .add_field(name="Passed", value=ahItems["passed"])
                                .add_field(
                                    name="Date Added",
                                    value=format_dt(
                                        parseDatetime(ahItems["date_added"])
                                    ),
                                )
                                for ahItems in userData["auction_house"]
                            ],
                            label="Auction House",
                            description="View the items you are selling at the Auction House",
                        )
                    )
                mainPages = pages.Paginator(pages=pageGroups, show_menu=True)
                await mainPages.respond(ctx.interaction, ephemeral=False)
        except ItemNotFound:
            embedError = discord.Embed()
            embedError.description = "It seems like that your account was not found. Please initialize your account first."
            return await ctx.respond(embed=embedError, ephemeral=True)

    @eco_users.command(name="inv")
    async def ecoUserInv(self, ctx):
        """Access your inventory"""
        try:
            userData = await cache.cacheUser(
                user_id=ctx.user.id, command_name=ctx.command.qualified_name
            )
            if userData is None:
                raise NoItemsError
            else:
                mainPages = pages.Paginator(
                    pages=[
                        discord.Embed(
                            title=items["name"], description=items["description"]
                        )
                        .add_field(name="Amount", value=items["amount"])
                        .add_field(
                            name="Date Acquired",
                            value=format_dt(parseDatetime(items["date_acquired"])),
                        )
                        for items in userData["user_inv"]
                    ],
                    loop_pages=True,
                )
                await mainPages.respond(ctx.interaction, ephemeral=False)
        except NoItemsError:
            embedTypeError = discord.Embed()
            embedTypeError.description = "It seems you don't have any items in your inventory! Start purchasing some items from the marketplace to get started!"
            await ctx.respond(embed=embedTypeError, ephemeral=True)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    @ecoUsersDelete.command(name="account")
    async def purgeUserAcct(self, ctx):
        """Permanently deletes your user eco account"""
        embed = discord.Embed()
        embed.description = "Do you want to delete your economy account? This is permanent and cannot be undone. Click on the buttons to confirm\nAny created quests, marketplace listings, inventory items and auction house listings will be deleted permanently as well."
        await ctx.respond(embed=embed, view=EcoUserPurgeView(), ephemeral=True)


def setup(bot):
    bot.add_cog(EcoUsers(bot))
