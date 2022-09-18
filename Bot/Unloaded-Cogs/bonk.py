import discord
from discord.commands import slash_command
from discord.ext import commands


class BonkV1(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(name="bonk", description="bonkkk")
    async def bonk_user(self, ctx):
        embedVar = discord.Embed()
        embedVar.description = f"Bonked {ctx.author.mention}"
        file = discord.File("./Bot/Cogs/images/bonk.gif")
        embedVar.set_image(url="attachment://bonk.gif")
        await ctx.respond(embed=embedVar, file=file)


def setup(bot):
    bot.add_cog(BonkV1(bot))
