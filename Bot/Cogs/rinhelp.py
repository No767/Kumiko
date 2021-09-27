import discord
import discord.ext
from discord.ext import commands


class rinhelp(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.last_member = None

    @commands.command(name="rinhelp", help="Rin's Help/Info Page")
    async def on_message(self, ctx):
        try:
            bot = self.bot
            name = bot.user.name
            id = bot.user.id
            embedVar = discord.Embed(title="Rin Help", color=14414079)
            embedVar.description = f"""
                    Help Section Page
                    """
            embedVar.set_thumbnail(url=bot.user.avatar_url)
            await ctx.send(embed=embedVar)
        except:
            bot = self.bot
            name = bot.user.name
            id = bot.user.id
            embedVar = discord.Embed(title="Rin Help", color=14414079)
            embedVar.description = f"""
                                The full list of commands can be found here: https://rin-docs.readthedocs.io/en/latest/rin-commands/
                                """
            embedVar.set_thumbnail(url=bot.user.avatar_url)
            await ctx.send(embed=embedVar)


class rinhelpv2(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


def setup(bot):
    bot.add_cog(rinhelp(bot))
    bot.add_cog(rinhelpv2(bot))
