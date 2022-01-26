import asyncio
import uvloop
import os
from dotenv import load_dotenv
import aiohttp
import ujson
from discord.ext import commands
import discord

load_dotenv()

OpenAI_API_KEY = os.getenv("OpenAI_API_Key")

class OpenAI1(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command(name="openai-complete", aliases=["ai-complete"])
    async def openaiComplete(self, ctx, *, completion=None):
        async with aiohttp.ClientSeession(json_serialize=ujson.dumps) as session:
            headers = {"Authorization": f"Bearer {OpenAI_API_KEY}", "Content-Type": "application/json"}
            payload = {"prompt": f"{completion}", "max_tokens": 32, "temperature": 0.35, "top_p": 0.20}
            async with session.post("https://api.openai.com/v1/engines/ada/completions", headers=headers, json=payload) as r:
                data = await r.json()
                embed = discord.Embed()
                print(data)
                embed.description = data["choices"]["text"]
                await ctx.send(embed=embed)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

def setup(bot):
    bot.add_cog(OpenAI1(bot))