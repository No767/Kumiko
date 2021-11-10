from discord.ext import commands
import discord


class rinpinger(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="pinger")
    async def pinger(self, ctx, replace: int, *, reason: str):
        try:
            for _ in range(replace):
                await ctx.send(f"@everyone {reason}")
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
