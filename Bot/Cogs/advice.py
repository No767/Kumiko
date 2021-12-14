<<<<<<< HEAD
import discord
import requests
=======
import aiohttp
import discord
>>>>>>> a5659c14a6103770ed114e62aee8a13b58a89b5d
import ujson
from discord.ext import commands


<<<<<<< HEAD
def advice():
    link = "https://api.adviceslip.com/advice"
    r = requests.get(link)
    return ujson.loads(r.text)


=======
>>>>>>> a5659c14a6103770ed114e62aee8a13b58a89b5d
class advice_slip(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="advice")
    async def on_message(self, ctx):
<<<<<<< HEAD
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
            embedVar.description = "The query failed. Please try again."
            embedVar.add_field(name="Reason", value=e, inline=True)
            await ctx.send(embed=embedVar)
=======
        async with aiohttp.ClientSession(json_serialize=ujson.dumps) as session:
            async with session.get(f"https://api.adviceslip.com/advice") as r:
                advice_slip = await r.text()
                try:
                    embedVar = discord.Embed(
                        color=discord.Color.from_rgb(251, 204, 255)
                    )
                    embedVar.description = f"{advice_slip['slip']['advice']}"
                    embedVar.set_footer(
                        text=f"Requested by {ctx.message.author.name}",
                        icon_url=ctx.message.author.avatar_url,
                    )
                    await ctx.send(embed=embedVar)
                except Exception as e:
                    embedVar = discord.Embed()
                    embedVar.description = "The query failed. Please try again."
                    embedVar.add_field(name="Reason", value=e, inline=True)
                    await ctx.send(embed=embedVar)
>>>>>>> a5659c14a6103770ed114e62aee8a13b58a89b5d


def setup(bot):
    bot.add_cog(advice_slip(bot))
