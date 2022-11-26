import asyncio
import os

import discord
import uvloop
from dateutil import parser
from discord.commands import SlashCommandGroup
from discord.ext import commands, pages
from dotenv import load_dotenv
from kumiko_economy import KumikoEcoUserUtils, KumikoUserInvUtils
from kumiko_ui_components import CreateAccountView, PurgeAccountView
from rin_exceptions import ItemNotFound, NoItemsError

load_dotenv()

POSTGRES_PASSWORD = os.getenv("Postgres_Password")
POSTGRES_SERVER_IP = os.getenv("Postgres_Server_IP")
POSTGRES_DATABASE = os.getenv("Postgres_Kumiko_Database")
POSTGRES_USERNAME = os.getenv("Postgres_Username")
POSTGRES_PORT = os.getenv("Postgres_Port")
CONNECTION_URI = f"postgresql+asyncpg://{POSTGRES_USERNAME}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER_IP}:{POSTGRES_PORT}/{POSTGRES_DATABASE}"

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
