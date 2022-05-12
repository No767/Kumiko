import asyncio
import re

import discord
import uvloop
from discord.commands import Option, SlashCommandGroup
from discord.ext import commands
from economy_utils import KumikoEcoUserUtils, UsersInv

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
        await utilsUser.insUserFirstTime(interaction.user.id)
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


class ecoUsers(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    eco_users = SlashCommandGroup(
        name="users",
        description="Commands for handling user-related data and transactions for Kumiko's economy system",
        guild_ids=[970159505390325842],
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
        mainBal = await utilsUser.getUser(ctx.user.id)
        embedVar = discord.Embed()
        embedVar.title = f"{await self.bot.fetch_user(mainBal[0])}"
        embedVar.add_field(name="Coins", value=mainBal[1], inline=True)
        embedVar.set_thumbnail(url=ctx.user.display_avatar)
        await ctx.respond(embed=embedVar)

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
        userInv = await inv.obtainInv(ctx.user.id)
        embed = discord.Embed()
        for items in userInv:
            mainDict = dict(items)
            mainItems = dict(mainDict["items"])
            for k, v in mainDict["items"]:
                if k not in ["name", "description"]:
                    embed.add_field(name=k, value=v, inline=True)
            embed.title = mainItems["name"]
            embed.description = mainItems["description"]
            embed.remove_field(-2)
            await ctx.respond(embed=embed)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


def setup(bot):
    bot.add_cog(ecoUsers(bot))
