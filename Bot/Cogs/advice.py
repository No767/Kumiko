import aiohttp
import discord
import ujson
from discord.ext import commands


class advice_slip(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="advice")
    async def on_message(self, ctx):
        async with aiohttp.ClientSession(json_serialize=ujson.dumps) as session:
            async with session.get("https://api.adviceslip.com/advice") as r:
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


def setup(bot):
    bot.add_cog(advice_slip(bot))
