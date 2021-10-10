from discord.ext import commands


class pinger(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Note that you need to wrap the message around in "" marks. Which is just making it a string
    @commands.command(name="pinger")
    async def on_message(self, ctx, replace:int, *,  reason: str):
        try:
            for x in range(replace):
                await ctx.send(f"@everyone {reason}")
        except Exception as e:
            await ctx.send(f"""
                           The pinger cog didnt work. Please try again.\n
                           Reason: {e}
                           """)


def setup(bot):
    bot.add_cog(pinger(bot))
