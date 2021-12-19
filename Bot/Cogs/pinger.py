import discord
from discord.ext import commands


class rinpinger(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="pinger")
    async def pinger(self, ctx):
        try:

            def check(ms):
                return ms.user == ctx.user.name and ctx.message.content != [
                    "@everyone",
                    "@here",
                ]

            await ctx.send("Enter the number of times you want to ping someone: ")
            ping = await self.bot.wait_for("message", check=check)
            await ctx.send("Enter the user you want to ping: ")
            user = await self.bot.wait_for("message", check=check)
            await ctx.send("Enter the reason for the ping: ")
            reason = await self.bot.wait_for("message", check=check)
            for _ in range(int(ping.content)):
                await ctx.send(f"{user} {reason}")
        except Exception as e:
            await ctx.send(f"The pinger cog didnt work. Please try again.\nReason: {e}")

    @pinger.error
    async def on_message_error(
        self, ctx: commands.Context, error: commands.CommandError
    ):
        if isinstance(error, commands.MissingRequiredArgument):
            embedVar = discord.Embed(color=discord.Color.from_rgb(255, 51, 51))
            embedVar.description = f"Missing a required argument: {error.param}"
            msg = await ctx.send(embed=embedVar, delete_after=10)
            await msg.delete(delay=10)


def setup(bot):
    bot.add_cog(rinpinger(bot))
