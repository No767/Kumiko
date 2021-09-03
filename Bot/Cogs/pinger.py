from discord.ext import commands


class pinger(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Note that you need to wrap the message around in "" marks. Which is just making it a string
    @commands.command(name="pinger")
    async def on_message(self, ctx, search: str, replace: int):
        pinger_search = search
        for x in range(replace):
            await ctx.send(f"@everyone {search}")
    async def on_error(self, ctx):
        await ctx.send(f'There is something wrong with the pinger module. Please Try Again...')
def setup(bot):
    bot.add_cog(pinger(bot))
