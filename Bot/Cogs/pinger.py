from discord.ext import commands


class rinpinger(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="pinger")
    async def on_message(self, ctx, replace: int, *, reason: str):
        try:
            for _ in range(replace):
                await ctx.send(f"@everyone {reason}")
        except Exception as e:
            await ctx.send(f"The pinger cog didnt work. Please try again.\nReason: {e}")


def setup(bot):
    bot.add_cog(rinpinger(bot))
