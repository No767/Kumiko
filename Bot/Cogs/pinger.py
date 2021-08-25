from discord.ext import commands


class pinger(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Note that you need to wrap the message around in "" marks. Which is just making it a string
    @commands.command(name="pinger")
    async def on_message(self, ctx, search: str):
        pinger_search = search
        for everyone in range(11):
            await ctx.send(f"@everyone {search}")


def setup(bot):
    bot.add_cog(pinger(bot))
