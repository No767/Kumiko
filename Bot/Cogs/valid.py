import asyncio

import discord
import uvloop
from discord.ext import commands


class valid(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="valid")
    async def on_message(message, ctx, search: str):
        try:
            user_search = search
            embedVar = discord.Embed(color=14414079)
            embedVar.description = f"""
            You are valid no matter what! You got this {user_search}! 
            I just want to tell you can do this! You have my support!
            """
            embedVar.set_footer(
                text=f"Requested by {ctx.message.author.name}",
                icon_url=ctx.message.author.avatar_url,
            )
            await ctx.send(embed=embedVar)
        except Exception as e:
            embedVar = discord.Embed(color=14414079)
            embedVar.description = (
                f"There seems to be an error. Please try again.\n Reason: {e}"
            )
            await ctx.send(embed=embedVar)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


def setup(bot):
    bot.add_cog(valid(bot))
