import asyncio
import random

import discord
import numpy as np
import uvloop
from discord.commands import SlashCommandGroup
from discord.ext import commands
from economy_utils import KumikoEcoUserUtils, UsersInv

utilsUser = KumikoEcoUserUtils()
inv = UsersInv()


class CoinEarnV1(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    coins = SlashCommandGroup(
        "coins", "Base commands for coins", guild_ids=[970159505390325842]
    )
    coinsEarn = coins.create_subgroup(
        "earn", "Earn coins", guild_ids=[970159505390325842]
    )

    @coinsEarn.command(name="beg")
    @commands.cooldown(1, 86400, commands.BucketType.user)
    async def coinEarnBeg(self, ctx):
        """Earn some coins by literally begging for coins!"""
        amountOfCoins = np.random.randint(low=0, high=250)
        coinsMessages = [
            f"Someone accidentally dropped a bag of coins, and inside was {amountOfCoins} coins inside! You've hit the jackpot!",
            f"Someone kindly gave you a bag of coins, and inside that bag, was {amountOfCoins} coins inside.",
            f"Someone dropped a bag of coins, and inside that bag, was {amountOfCoins} coins inside.",
            f"You were begging for coins, and you went ahead to see what that purse inside was missing. Inside, you see a bag of coins, and you find {amountOfCoins} coins inside.",
        ]
        if amountOfCoins > 100:
            coinRandomMessage = random.choice(coinsMessages)  # nosec B311
        author_id = ctx.author.id
        userInfo = await utilsUser.getUser(user_id=author_id)
        totalAmountOfCoins = userInfo[1] + amountOfCoins
        await utilsUser.updateUser(owner_id=author_id, coins=totalAmountOfCoins)
        embedMain = discord.Embed()
        embedMain.description = (
            f"You were able to earn {amountOfCoins} coins! {coinRandomMessage}"
        )
        await ctx.respond(embed=embedMain)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


def setup(bot):
    bot.add_cog(CoinEarnV1(bot))
