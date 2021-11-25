import discord
import requests
import ujson
from discord.ext import commands


def advice():
    link = "https://api.adviceslip.com/advice"
    r = requests.get(link)
    return ujson.loads(r.text)


class advice_slip(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="advice")
    async def on_message(self, ctx):
        advice_slip = advice()
        try:
            embedVar = discord.Embed(
                color=discord.Color.from_rgb(251, 204, 255))
            embedVar.description = f"{advice_slip['slip']['advice']}"
            embedVar.set_footer(
                text=f"Requested by {ctx.message.author.name}",
                icon_url=ctx.message.author.avatar_url,
            )
            await ctx.send(embed=embedVar)
        except Exception as e:
            embedVar = discord.Embed()
            embedVar.description = f"""
            The query was unsuccessful
            Reason: {e}
            """
            await ctx.send(embed=embedVar)


def setup(bot):
    bot.add_cog(advice_slip(bot))
