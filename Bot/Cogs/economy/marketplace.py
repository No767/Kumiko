import os
from typing import Optional

import discord
from beanie import Document
from discord.commands import Option, slash_command
from discord.ext import commands
from dotenv import load_dotenv
from .utils import KumikoEcoUtils
import uvloop
import asyncio

load_dotenv()
utilsMain = KumikoEcoUtils()
MongoDB_Password = os.getenv("MongoDB_Password")
Username = os.getenv("MongoDB_Username")
Server_IP = os.getenv("MongoDB_Server_IP")


class Marketplace(Document):
    name: str
    description: Optional[str] = None
    amount: int


# class Auth(discord.ui.Button):
#     def __init__(self):
#         super().__init__()
#         self.value = None

#     async def callback(self, interaction: discord.Interaction):
#         view: ecoMarketplace = self.view
#         await interaction.response.send_message(
#             "Confirmed. Now you have access to the marketplace", ephemeral=True
#         )
#         self.value = True
#         self.stop()


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
        await ctx.respond(embed=embed)


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
        amount: Option(int, "The amount of the item you wish to add")
    ):
        await utilsMain.ins(name, description, amount)
        await ctx.respond("Item added to the marketplace")
    
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
class ecoView(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @slash_command(name="eco-marketplace-view", description="View the marketplace", guild_ids=[866199405090308116])
    async def ecoMarketplaceView(self, ctx):
        mainObtain = await utilsMain.obtain()
        filter = ["revision_id", "id", "description", "name"]
        embed = discord.Embed()
        for items in mainObtain:
            mainDict = dict(items)
            for keys, value in mainDict.items():
                if keys not in filter:
                    embed.add_field(name=keys, value=value, inline=True)
                    embed.remove_field(-2)
                embed.title = mainDict["name"]
                embed.description = mainDict["description"]
                
            await ctx.respond(embed=embed)
            
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

class ecoSearch(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @slash_command(name="eco-marketplace-search", description="Search the marketplace", guild_ids=[866199405090308116])
    async def ecoMarketplaceSearch(self, ctx, *, name: Option(str, "The name of the item you wish to search")):
        mainGetItem = await utilsMain.getItem(name)
        filterTheThird = ["revision_id", "id", "description", "name"]
        embed = discord.Embed()
        print(mainGetItem)
        for k, v, in dict(mainGetItem).items():
            if k not in filterTheThird:
                embed.add_field(name=k, value=v, inline=True)
                embed.remove_field(-2)
            embed.title = dict(mainGetItem)["name"]
            embed.description = dict(mainGetItem)["description"]
            
        await ctx.respond(embed=embed)
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())        

def setup(bot):
    bot.add_cog(ecoMarketplace(bot))
    bot.add_cog(ecoAdd(bot))
    bot.add_cog(ecoView(bot))
    bot.add_cog(ecoSearch(bot))
