import asyncio
import os
import re

import discord
import numpy as np
import uvloop
from discord.commands import Option, SlashCommandGroup
from discord.ext import commands
from dotenv import load_dotenv
from economy_utils import KumikoEcoUserUtils
from numpy.random import default_rng
from rin_exceptions import ItemNotFound

rng = default_rng()

load_dotenv()

POSTGRES_PASSWORD = os.getenv("Postgres_Password_Dev")
POSTGRES_SERVER_IP = os.getenv("Postgres_Server_IP_Dev")
POSTGRES_DATABASE = os.getenv("Postgres_Database_Dev")
POSTGRES_USERNAME = os.getenv("Postgres_Username_Dev")
CONNECTION_URI = f"postgresql+asyncpg://{POSTGRES_USERNAME}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER_IP}:5432/{POSTGRES_DATABASE}"

utilsUser = KumikoEcoUserUtils()


class PetalEarnV1(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    petals = SlashCommandGroup(
        "petals", "Base commands for petals", guild_ids=[970159505390325842]
    )
    petalsEarn = petals.create_subgroup(
        "earn", "Earn petals", guild_ids=[970159505390325842]
    )

    @petalsEarn.command(name="beg")
    @commands.cooldown(1, 86400, commands.BucketType.user)
    async def coinEarnBeg(self, ctx):
        """Earn some Lavender Petals by literally begging for Lavender Petals!"""
        amountOfPetals = np.random.randint(low=0, high=250)
        petalsMessages = np.array(
            [
                f"Someone accidentally dropped a sack of Lavender Petals, and inside was {amountOfPetals} Petals inside! You've hit the jackpot!",
                f"Someone kindly gave you a sack of Lavender Petals, and inside that sack, was {amountOfPetals} Petals inside.",
                f"Someone dropped a sack of Lavender Petals, and inside that sack, was {amountOfPetals} Petals inside.",
                f"You were begging for Lavender Petals, and you went ahead to see what that purse inside was missing. Inside, you see a sack of Lavender Petals, and you find {amountOfPetals} Petals inside.",
            ]
        )
        if amountOfPetals > 100:
            petalRandomMessage = rng.choice(petalsMessages)  # nosec B311
            author_id = ctx.author.id
            userInfo = await utilsUser.obtainUserData(
                user_id=author_id, uri=CONNECTION_URI
            )
            for items in userInfo:
                mainItems = dict(items)
            totalAmountOfPetals = mainItems["lavender_petals"] + amountOfPetals
            await utilsUser.updateUserLavenderPetals(
                author_id, totalAmountOfPetals, CONNECTION_URI
            )
            embedMain = discord.Embed()
            embedMain.description = (
                f"You were able to earn {amountOfPetals} Petals! {petalRandomMessage}"
            )
            await ctx.respond(embed=embedMain)
        else:
            userInfo = await utilsUser.obtainUserData(
                user_id=author_id, uri=CONNECTION_URI
            )
            for items in userInfo:
                mainItems = dict(items)
            totalAmountOfPetals = mainItems["lavender_petals"] + amountOfPetals
            await utilsUser.updateUserLavenderPetals(
                author_id, totalAmountOfPetals, CONNECTION_URI
            )
            embedMain = discord.Embed()
            embedMain.description = f"You were able to earn {amountOfPetals} Petals!"
            await ctx.respond(embed=embedMain)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    @petals.command(name="trade")
    async def tradePetals(
        self,
        ctx,
        *,
        receiver: Option(str, "The receiver you wish to send to"),
        amount: Option(int, "The amount to transfer"),
    ):
        """Alows the trade of petals betweens the users"""
        if receiver > 100:
            await ctx.respond("Sadly you can't transfer that much petals...")
        else:
            sortedReceiverID = int(re.sub("[^a-zA-Z0-9 ]", "", receiver))
            currentUser = await utilsUser.obtainUserData(ctx.author.id, CONNECTION_URI)
            receivingUser = await utilsUser.obtainUserData(
                sortedReceiverID, CONNECTION_URI
            )
            try:
                if len(currentUser) == 0 or len(receivingUser) == 0:
                    raise ItemNotFound
                else:
                    for items in currentUser:
                        mainItems = dict(items)
                    for receiverItems in receivingUser:
                        mainReceiverItems = dict(receiverItems)
                    currentUserLavenderPetals = mainItems["lavender_petals"]
                    receivingUserLavenderPetals = mainReceiverItems["lavender_petals"]
                    totalAmountSender = currentUserLavenderPetals - amount
                    totalAmountReceiver = receivingUserLavenderPetals + amount
                    await utilsUser.updateUserLavenderPetals(
                        ctx.author.id, totalAmountSender, CONNECTION_URI
                    )
                    await utilsUser.updateUserLavenderPetals(
                        sortedReceiverID, totalAmountReceiver, CONNECTION_URI
                    )
                    await ctx.respond("Successfully traded the Lavender Petals!")
            except ItemNotFound:
                embedError = discord.Embed()
                embedError.description = (
                    "It seems like that either one of the accounts were not made."
                )


def setup(bot):
    bot.add_cog(PetalEarnV1(bot))
