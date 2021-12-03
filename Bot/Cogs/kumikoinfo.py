import discord
from discord.ext import commands
from discord_components import Button


class info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="kumiko-info", help="Server Info")
    async def on_message(self, message):
        bot = self.bot
        embedVar = discord.Embed(color=14414079)
        embedVar.set_author(name="Kumiko Info", icon_url=bot.user.avatar_url)
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
            text="Project Lead Maintainer and Original Creator of Rin and Kumiko: No767\nOriginal Creator of EasyBot.py and EasyBot Plugins: Chisaku-dev"
        )
        await message.channel.send(
            embed=embedVar,
            components=[
                [
                    Button(label="GitHub",
                           url="https://github.com/No767/Kumiko", style=5),
                    Button(
                        label="Issue Tracker",
                        url="https://github.com/No767/Kumiko/issues",
                        style=5,
                    ),
                    Button(
                        label="Docs",
                        url="https://rin-docs.readthedocs.io/en/latest",
                        style=5,
                    ),
                    Button(
                        label="Invite",
                        url="https://top.gg/bot/865883525932253184/invite",
                        style=5,
                    ),
                    Button(label="Website", url="https://rinbot.live", style=5),
                ]
            ],
        )


def setup(bot):
    bot.add_cog(info(bot))
