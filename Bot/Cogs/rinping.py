import discord
from discord.ext import commands


class rinping(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name="ping",
    )
    async def on_message(self, ctx):
        try:
            ping_embed = discord.Embed()
            ping_embed.description = f"Ping >> {round(self.bot.latency * 1000)} ms"
            await ctx.send(embed=ping_embed)
        except Exception as e:
            ping_embed = discord.Embed()
            ping_embed.description = f"The command was not successful\n Reason: {e}"
            await ctx.send(embed=ping_embed)


def setup(bot):
    bot.add_cog(rinping(bot))
