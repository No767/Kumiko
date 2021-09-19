import discord
from discord.ext import commands
import discord.ext


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
        
    @commands.command(name="helpv2")
    async def on_message(self, ctx, *, args):
        try: 
            if str(args) == "help":
                bot = self.bot
                name = bot.user.name
                id = bot.user.id
                embedVar = discord.Embed(title="Rin Help", color=14414079)
                embedVar.description = f"""
                For the time being, this is still being worked on. 
                Actually adding them in and formatting them into the right places is going to take a lot of time.
                Which i really dont have          
                """
                embedVar.set_thumbnail(url=bot.user.avatar_url)
                await ctx.send(embed=embedVar)
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


def setup(bot):
    bot.add_cog(rinhelp(bot))
    bot.add_cog(rinhelpv2(bot))
