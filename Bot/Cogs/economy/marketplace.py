import asyncio

import discord
import uvloop
from discord.commands import Option, slash_command, SlashCommandGroup
from discord.ext import commands
from economy_utils import KumikoEcoUtils
from datetime import datetime

utilsMain = KumikoEcoUtils()
today = datetime.now()



class ecoMarketplace(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    eco_marketplace = SlashCommandGroup(name="marketplace", description="Commands for Kumiko's Marketplace", guild_ids=[970159505390325842])
    
    @eco_marketplace.command(
        name="add-item"
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
        """Adds an item into the marketplace"""
        dateEntry = today.strftime("%B %d, %Y %H:%M:%S")
        owner = ctx.user.id
        await utilsMain.ins(dateEntry, owner, name, description, amount, price)
        await ctx.respond("Item added to the marketplace")
        
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    @eco_marketplace.command(name="view")
    async def ecoMarketplaceView(self, ctx):
        """View the marketplace"""
        mainObtain = await utilsMain.obtain()
        filter = ["revision_id", "id", "description", "name"]
        embed = discord.Embed()
        for items in mainObtain:
            mainDict = dict(items)
            for keys, value in mainDict.items():
                if keys not in filter:
                    embed.add_field(name=keys, value=value, inline=True)
                    embed.remove_field(-5)
                embed.title = mainDict["name"]
                embed.description = mainDict["description"]

            await ctx.respond(embed=embed)
            
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
            
    @eco_marketplace.command(
        name="search",
    )
    async def ecoMarketplaceSearch(
        self, ctx, *, name: Option(str, "The name of the item you wish to search")
    ):
        """Search the marketplace"""
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





def setup(bot):
    bot.add_cog(ecoMarketplace(bot))

