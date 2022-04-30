import asyncio
import os

import discord
import uvloop
from discord.commands import Option, slash_command
from discord.ext import commands
from dotenv import load_dotenv
from economy_utils import KumikoEcoUserUtils, KumikoEcoUtils

load_dotenv()

utilsMain = KumikoEcoUtils()
utilsUser = KumikoEcoUserUtils()

MongoDB_Password = os.getenv("MongoDB_Password")
Username = os.getenv("MongoDB_Username")
Server_IP = os.getenv("MongoDB_Server_IP")


class View(discord.ui.View):
    @discord.ui.button(
        label="Yes", row=0, style=discord.ButtonStyle.primary, emoji="✔️"
    )
    async def button_callback(self, button, interaction):
        await utilsUser.insUserFirstTime(interaction.user.id)
        await interaction.response.send_message(
            "Confirmed. Now you have access to the marketplace!"
        )

    @discord.ui.button(label="No", row=0, style=discord.ButtonStyle.primary, emoji="❌")
    async def second_button_callback(self, button, interaction):
        await interaction.response.send_message("Welp, you choose not to ig...")


class ecoMarketplace(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(
        name="eco-init",
        description="Initialize your user account",
        guild_ids=[866199405090308116],
    )
    async def ecoInit(self, ctx):
        embed = discord.Embed()
        embed.description = "Do you wish to initialize your economy account? This is completely optional. Click on the buttons to confirm"
        await ctx.respond(embed=embed, view=View())


class ecoAdd(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(
        name="eco-add-item",
        description="Add an item to the marketplace",
        guild_ids=[866199405090308116],
    )
    async def ecoAddItem(
        self,
        ctx,
        *,
        name: Option(str, "The name of the item you wish to add"),
        description: Option(str, "The description of the item you wish to add"),
        amount: Option(int, "The amount you are willing to sell"),
        price: Option(int, "The price of the item")
    ):
        await utilsMain.ins(name, description, amount, price)
        await ctx.respond("Item added to the marketplace")

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


class ecoView(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(
        name="eco-marketplace-view",
        description="View the marketplace",
        guild_ids=[866199405090308116],
    )
    async def ecoMarketplaceView(self, ctx):
        mainObtain = await utilsMain.obtain()
        filter = ["revision_id", "id", "description", "name"]
        embed = discord.Embed()
        for items in mainObtain:
            mainDict = dict(items)
            for keys, value in mainDict.items():
                if keys not in filter:
                    embed.add_field(name=keys, value=value, inline=True)
                    embed.remove_field(-3)
                embed.title = mainDict["name"]
                embed.description = mainDict["description"]

            await ctx.respond(embed=embed)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


class ecoSearch(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(
        name="eco-marketplace-search",
        description="Search the marketplace",
        guild_ids=[866199405090308116],
    )
    async def ecoMarketplaceSearch(
        self, ctx, *, name: Option(str, "The name of the item you wish to search")
    ):
        mainGetItem = await utilsMain.getItem(name)
        filterTheThird = ["revision_id", "id", "description", "name"]
        embed = discord.Embed()
        print(mainGetItem)
        for (
            k,
            v,
        ) in dict(mainGetItem).items():
            if k not in filterTheThird:
                embed.add_field(name=k, value=v, inline=True)
                embed.remove_field(-2)
            embed.title = dict(mainGetItem)["name"]
            embed.description = dict(mainGetItem)["description"]

        await ctx.respond(embed=embed)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


class ecoUserBal(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(
        name="eco-balance",
        description="Check the user's balance",
        guild_ids=[866199405090308116],
    )
    async def ecoBal(self, ctx):
        mainBal = await utilsUser.getUser(ctx.user.id)
        print(mainBal)
        embedVar = discord.Embed()
        embedVar.title = mainBal[0]
        embedVar.add_field(name="Coins", value=mainBal[1], inline=True)
        await ctx.respond(embed=embedVar)


def setup(bot):
    bot.add_cog(ecoMarketplace(bot))
    bot.add_cog(ecoAdd(bot))
    bot.add_cog(ecoView(bot))
    bot.add_cog(ecoSearch(bot))
    bot.add_cog(ecoUserBal(bot))
