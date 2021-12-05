import discord
from discord.ext import commands


class ErrorHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(
        self, ctx: commands.Context, error: commands.CommandError
    ):
        if isinstance(error, commands.MissingPermissions):
            embedVar = discord.Embed(
                color=discord.Color.from_rgb(226, 199, 255))
            embedVar.description = (
                f"You are missing the following permissions: {error.missing_perms}"
            )
            msg = await ctx.send(embed=embedVar, delete_after=10)
            await msg.delete(delay=10)
        elif isinstance(error, commands.BotMissingPermissions):
            embedVar = discord.Embed(
                color=discord.Color.from_rgb(226, 199, 255))
            embedVar.description = f"{self.bot.user.name} is currently missing the following permissions: {error.missing_perms}"
            msg = await ctx.send(embed=embedVar, delete_after=10)
            await msg.delete(delay=10)
        elif isinstance(error, commands.MissingAnyRole):
            embedVar = discord.Embed(
                color=discord.Color.from_rgb(226, 199, 255))
            embedVar.description = (
                f"You are missing the following roles: {error.missing_roles}"
            )
            msg = await ctx.send(embed=embedVar, delete_after=10)
            await msg.delete(delay=10)
        elif isinstance(error, commands.BotMissingAnyRole):
            embedVar = discord.Embed(
                color=discord.Color.from_rgb(226, 199, 255))
            embedVar.description = f"{self.bot.user.name} is currently missing the following roles: {error.missing_roles}"
            msg = await ctx.send(embed=embedVar, delete_after=10)
            await msg.delete(delay=10)

# Remove this again due to discord.bots.gg testing
# if isinstance(error, commands.CommandNotFound):
#     embedVar = discord.Embed(
#         color=discord.Color.from_rgb(226, 199, 255))
#     embedVar.description = f"{error}. Please try again, or refer to either `rinhelp` or the [docs](https://rin-docs.readthedocs.io/en/latest)"
#     msg = await ctx.send(embed=embedVar, delete_after=10)
#     await msg.delete(delay=10)
def setup(bot):
    bot.add_cog(ErrorHandler(bot))
