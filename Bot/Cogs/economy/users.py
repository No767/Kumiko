import asyncio
import os
import re

import discord
import uvloop
from dateutil import parser
from discord.commands import Option, SlashCommandGroup
from discord.ext import commands, pages
from dotenv import load_dotenv
from economy_utils import KumikoEcoUserUtils, UsersInv
from rin_exceptions import ItemNotFound, NoItemsError

load_dotenv()

POSTGRES_PASSWORD = os.getenv("Postgres_Password_Dev")
POSTGRES_SERVER_IP = os.getenv("Postgres_Server_IP_Dev")
POSTGRES_DATABASE = os.getenv("Postgres_Database_Dev")
POSTGRES_USERNAME = os.getenv("Postgres_Username_Dev")
CONNECTION_URI = f"postgresql+asyncpg://{POSTGRES_USERNAME}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER_IP}:5432/{POSTGRES_DATABASE}"

utilsUser = KumikoEcoUserUtils()
inv = UsersInv()


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
        await utilsUser.initUserAcct(interaction.user.id, CONNECTION_URI)
        await interaction.response.send_message(
            "Confirmed. Now you have access to the marketplace!"
        )

    @discord.ui.button(
        label="No",
        row=0,
        style=discord.ButtonStyle.primary,
        emoji=discord.PartialEmoji.from_str("<:xmark:314349398824058880>"),
    )
    async def second_button_callback(self, button, interaction):
        await interaction.response.send_message("Welp, you choose not to ig...")


class PurgeView(discord.ui.View):
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
        await utilsUser.deleteUser(interaction.user.id, CONNECTION_URI)
        await interaction.response.send_message(
            "Confirmed. Your have permanently deleted your account."
        )

    @discord.ui.button(
        label="No",
        row=0,
        style=discord.ButtonStyle.primary,
        emoji=discord.PartialEmoji.from_str("<:xmark:314349398824058880>"),
    )
    async def second_button_callback(self, button, interaction):
        await interaction.response.send_message("Welp, you choose not to ig...")


class ecoUsers(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    eco_users = SlashCommandGroup(
        name="users",
        description="Commands for handling user-related data and transactions for Kumiko's economy system",
        guild_ids=[970159505390325842],
    )
    ecoUsersDelete = eco_users.create_subgroup(
        "delete", "Delete user data", guild_ids=[970159505390325842]
    )

    @eco_users.command(name="init")
    async def ecoInit(self, ctx):
        """Initialize your user account"""
        embed = discord.Embed()
        embed.description = "Do you wish to initialize your economy account? This is completely optional. Click on the buttons to confirm"
        await ctx.respond(embed=embed, view=View())

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    @eco_users.command(name="balance")
    async def ecoBal(self, ctx):
        """Gets your user balance profile"""
        mainBal = await utilsUser.obtainUserData(ctx.user.id, CONNECTION_URI)
        try:
            if len(mainBal) == 0:
                raise ItemNotFound
            else:
                for items in mainBal:
                    mainItem = dict(items)
                    getUser = await self.bot.get_or_fetch_user(mainItem["user_id"])
                    embedVar = discord.Embed()
                    embedVar.title = getUser.name
                    embedVar.add_field(
                        name="Lavender Petals",
                        value=mainItem["lavender_petals"],
                        inline=True,
                    )
                    embedVar.set_thumbnail(url=ctx.user.display_avatar)
                    await ctx.respond(embed=embedVar)
        except ItemNotFound:
            embedError = discord.Embed()
            embedError.description = "It seems like that your account was not found. Please initialize your account first."
            await ctx.respond(embed=embedError)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    @eco_users.command(name="profile")
    async def ecoProfile(self, ctx):
        """Gets your user economy profile"""
        mainProfile = await utilsUser.obtainUserData(ctx.user.id, CONNECTION_URI)
        try:
            if len(mainProfile) == 0:
                raise ItemNotFound
            else:
                for items in mainProfile:
                    mainItem = dict(items)
                    getUser = await self.bot.get_or_fetch_user(mainItem["user_id"])
                    embedVar = discord.Embed()
                    embedVar.title = getUser.name
                    embedVar.add_field(
                        name="Lavender Petals",
                        value=mainItem["lavender_petals"],
                        inline=True,
                    )
                    embedVar.add_field(name="Rank", value=mainItem["rank"], inline=True)
                    embedVar.add_field(
                        name="Date Joined",
                        value=parser.isoparse(mainItem["date_joined"]).strftime(
                            "%Y-%m-%d %H:%M:%S"
                        ),
                        inline=True,
                    )
                    embedVar.set_thumbnail(url=ctx.user.display_avatar)
                    await ctx.respond(embed=embedVar)
        except ItemNotFound:
            embedError = discord.Embed()
            embedError.description = "It seems like that your account was not found. Please initialize your account first."
            await ctx.respond(embed=embedError)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    @eco_users.command(name="transfer")
    async def ecoUserTransaction(
        self,
        ctx,
        *,
        user: Option(str, "The user you wish to trade with"),
        amount: Option(int, "How much coins you wish to make in the transaction"),
    ):
        """Transfer a set amount of coins to another user"""
        sortedReceiver = int(re.sub("[^a-zA-Z0-9 ]", "", user))
        senderID = ctx.user.id
        obtainUserCoins = await utilsUser.getUser(senderID)
        obtainReceiverCoins = await utilsUser.getUser(sortedReceiver)
        totalAmountSender = obtainUserCoins[1] - amount
        totalAmountReceiver = obtainReceiverCoins[1] + amount
        await utilsUser.userTransaction(
            sender_id=senderID,
            receiver_id=sortedReceiver,
            sender_amount=totalAmountSender,
            receiver_amount=totalAmountReceiver,
        )
        embed = discord.Embed()
        embed.description = "Transaction made!"
        embed.add_field(
            name="Total balance for sender", value=totalAmountSender, inline=True
        )
        embed.add_field(
            name="Total balance for receiver", value=totalAmountReceiver, inline=True
        )
        await ctx.respond(embed=embed)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    @eco_users.command(name="inv")
    async def ecoUserInv(self, ctx):
        """Access your inventory"""
        try:
            userInv = await inv.obtainUserInv(ctx.user.id)
            if len(userInv) == 0:
                raise NoItemsError
            else:
                mainPages = pages.Paginator(
                    pages=[
                        discord.Embed(
                            title=dict(dictItem)["items"]["name"],
                            description=dict(dictItem)["items"]["description"],
                        ).add_field(
                            name="Amount",
                            value=dict(dictItem)["items"]["amount"],
                            inline=True,
                        )
                        for dictItem in userInv
                    ],
                    loop_pages=True,
                )
                await mainPages.respond(ctx.interaction, ephemeral=False)
        except NoItemsError:
            embedTypeError = discord.Embed()
            embedTypeError.description = "It seems you don't have any items in your inventory! Start purchasing some items from the marketplace to get started!"
            await ctx.respond(embed=embedTypeError)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    @ecoUsersDelete.command(name="account")
    async def purgeUserAcct(self, ctx):
        """Permanently deletes your user eco account"""
        embed = discord.Embed()
        embed.description = "Do you really want to delete your eco account? This is a permanent action and cannot be undone. Click on the buttons to confirm"
        await ctx.respond(embed=embed, view=PurgeView())


def setup(bot):
    bot.add_cog(ecoUsers(bot))
