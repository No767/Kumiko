import asyncio
import os

import discord
import numpy as np
import uvloop
from discord.commands import SlashCommandGroup
from discord.ext import commands
from dotenv import load_dotenv
from kumiko_economy import KumikoEcoUserUtils
from numpy.random import default_rng
from rin_exceptions import ItemNotFound

rng = default_rng()

load_dotenv()

POSTGRES_PASSWORD = os.getenv("Postgres_Password")
POSTGRES_SERVER_IP = os.getenv("Postgres_Server_IP")
POSTGRES_DB = os.getenv("Postgres_Kumiko_Database")
POSTGRES_SERVER_PORT = os.getenv("Postgres_Port")
POSTGRES_USERNAME = os.getenv("Postgres_Username")

USERS_CONNECTION_URI = f"postgresql+asyncpg://{POSTGRES_USERNAME}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER_IP}:{POSTGRES_SERVER_PORT}/{POSTGRES_DB}"

utilsUser = KumikoEcoUserUtils()


class Petals(commands.Cog):
    """Earn and spend some of your Petals here!"""

    def __init__(self, bot):
        self.bot = bot

    petals = SlashCommandGroup("eco-petals", "Base commands for petals")
    petalsEarn = petals.create_subgroup("earn", "Earn petals")

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
        getUser = await utilsUser.getFirstUser(
            user_id=ctx.author.id, uri=USERS_CONNECTION_URI
        )
        try:
            if getUser is None:
                raise ItemNotFound
            else:
                totalAmountOfPetals = dict(getUser)["lavender_petals"] + amountOfPetals
                await utilsUser.updateUserLavenderPetals(
                    user_id=ctx.author.id,
                    lavender_petals=totalAmountOfPetals,
                    uri=USERS_CONNECTION_URI,
                )
                if amountOfPetals > 100:
                    await ctx.respond(
                        embed=discord.Embed(
                            description=f"You were able to earn {amountOfPetals} Petals! {rng.choice(petalsMessages)}"
                        )
                    )
                else:
                    await ctx.respond(
                        embed=discord.Embed(
                            description=f"You were able to earn {amountOfPetals} Petals!"
                        )
                    )
        except ItemNotFound:
            embedError = discord.Embed()
            embedError.description = "Apparently you may have not created an economy account first. Please do that first."
            await ctx.respond(embed=embedError)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


def setup(bot):
    bot.add_cog(Petals(bot))
