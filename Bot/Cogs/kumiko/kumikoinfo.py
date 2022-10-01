import discord
from discord.ext import commands


class info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="kumiko-info", help="Server Info")
    async def on_message(self, ctx):
        bot = self.bot
        embedVar = discord.Embed(color=14414079)
        embedVar.set_author(name="Kumiko Info", icon_url=bot.user.display_avatar)
        embedVar.add_field(
            name="About",
            value="Kumiko is a multipurpose bot based off of [Rin](https://github.com/No767/Rin). It has all of the features of Rin, but with more features that are not third-party service related. Planned features includes moderation, and much much more.",
            inline=False,
        )
        embedVar.add_field(
            name="Getting Started",
            value="To help you get started, type in `.kumikohelp` or `.help` in order to access the help page. This will provide you with all of the commands that is available to use as of now.",
            inline=False,
        )
        embedVar.add_field(
            name="Questions or Issues?",
            value="If you have any questions, or any issues, or just an idea that you would like to add, please report them on the [GitHub Issue Tracker](https://github.com/No767/Kumiko/issues). Note that Kumiko does not any type of support discord server nor do I plan to make one to begin with.",
        )
        embedVar.set_footer(
            text="Project Lead Maintainer and Original Creator of Rin and Kumiko: No767\nOriginal Creator of EasyBot.py and EasyBot Plugins: Isaac-To"
        )
        await ctx.send(embed=embedVar)


def setup(bot):
    bot.add_cog(info(bot))
