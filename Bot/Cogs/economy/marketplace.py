from utils import KumikoEcoUtils

from typing import Optional
from beanie import Document
from beanie import init_beanie
from dotenv import load_dotenv
import os
import motor.motor_asyncio
import discord
from discord.commands import Option, slash_command
from discord.ext import commands

load_dotenv()
utils = KumikoEcoUtils()
MongoDB_Password = os.getenv("MongoDB_Password")
Username = os.getenv("MongoDB_Username")
Server_IP = os.getenv("MongoDB_Server_IP")


class Marketplace(Document):
    name: str
    description: Optional[str] = None
    amount: int


class Auth(discord.ui.Button):
    def __init__(self):
        super().__init__()
        self.value = None

    async def callback(self, interaction: discord.Interaction):
        view: ecoMarketplace = self.view
        await interaction.response.send_message(
            "Confirmed. Now you have access to the marketplace", ephemeral=True
        )
        self.value = True
        self.stop()


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
        await ctx.respond(embed=embed, view=Auth())


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
        # await utils.ins(name, description, amount)
        await ctx.respond("Item added to the marketplace")


def setup(bot):
    bot.add_cog(ecoMarketplace(bot))
    bot.add_cog(ecoAdd(bot))
