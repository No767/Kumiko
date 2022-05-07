import asyncio

import discord
import uvloop
from discord.commands import slash_command
from discord.ext import commands
from economy_utils import KumikoEcoUserUtils

utilsUser = KumikoEcoUserUtils()


class View(discord.ui.View):
    async def on_timeout(self):
        for child in self.children:
            child.disabled = True
            
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


class ecoInit(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(
        name="eco-init",
        description="Initialize your user account",
    )
    async def ecoInit(self, ctx):
        embed = discord.Embed()
        embed.description = "Do you wish to initialize your economy account? This is completely optional. Click on the buttons to confirm"
        await ctx.respond(embed=embed, view=View())


class ecoUserBal(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(
        name="eco-balance",
        description="Check the user's balance",
        guild_ids=[970159505390325842],
    )
    async def ecoBal(self, ctx):
        mainBal = await utilsUser.getUser(ctx.user.id)
        embedVar = discord.Embed()
        embedVar.title = f"{await self.bot.fetch_user(mainBal[0])}"
        embedVar.add_field(name="Coins", value=mainBal[1], inline=True)
        embedVar.set_thumbnail(url=ctx.user.display_avatar)
        await ctx.respond(embed=embedVar)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


def setup(bot):
    bot.add_cog(ecoInit(bot))
    bot.add_cog(ecoUserBal(bot))
