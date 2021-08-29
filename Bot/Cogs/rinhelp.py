import discord
from discord.ext import commands


class rinhelp(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="rinhelp")
    async def on_message(self, ctx, search: str):
        if search == "help":
            bot = self.bot
            name = bot.user.name
            id = bot.user.id
            embedVar = discord.Embed(title="Rin Help", color=14414079)
            embedVar.description = f"""
                Help Section Page
                """
            embedVar.set_thumbnail(url=bot.user.avatar_url)
            ctx.send(embed=embedVar)
        else:
            bot = self.bot
            name = bot.user.name
            id = bot.user.id
            embedVar = discord.Embed(title="Rin Help", color=14414079)
            embedVar.description = f"""
                The full list of commands can be found here: https://rin-docs.readthedocs.io/en/latest/rin-commands/
                """
        embedVar.set_thumbnail(url=bot.user.avatar_url)
        await ctx.send(embed=embedVar)

    async def error_message(self, ctx):
        bot = self.bot
        name = bot.user.name
        id = bot.user.id
        embedVar = discord.Embed(title="Rin Help", color=14414079)
        embedVar.description = f"""
            Sorry, try again. Something went wrong....
            """
        embedVar.set_thumbnail(url=bot.user.avatar_url)
        await ctx.send(embed=embedVar)


def setup(bot):
    bot.add_cog(rinhelp(bot))
