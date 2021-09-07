from discord.ext import commands
import discord


class Invite(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name="invite", help="Generates the link to invite bot", pass_context=True
    )
    async def invite(self, ctx):
        await ctx.send(
            f"https://discord.com/oauth2/authorize?client_id={self.bot.user.id}&scope=bot&permissions=8"
        )


def setup(bot):
    bot.add_cog(Invite(bot))
