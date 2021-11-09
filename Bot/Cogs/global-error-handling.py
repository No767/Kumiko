import discord
from discord.ext import commands


class ErrorHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(
        self, ctx: commands.Context, error: commands.CommandError
    ):
        if isinstance(error, commands.CommandNotFound):
            embedVar = discord.Embed(
                color=discord.Color.from_rgb(226, 199, 255))
            embedVar.description = f"The command that you were looking for doesn't exist. Please try again, or refer to either `rinhelp` or the [docs](https://rin-docs.readthedocs.io/en/latest)"
            msg = await ctx.send(embed=embedVar, delete_after=10)
            await msg.delete(delay=10)


def setup(bot):
    bot.add_cog(ErrorHandler(bot))
