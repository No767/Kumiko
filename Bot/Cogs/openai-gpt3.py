import asyncio
import os

import aiohttp
import discord
import ujson
import uvloop
from discord.ext import commands
from discord.commands import slash_command, Option
from dotenv import load_dotenv

load_dotenv()

OpenAI_API_KEY = os.getenv("OpenAI_API_Key")


class OpenAI1(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @slash_command(name="openai-complete", description="Completes a sentence using OpenAI's GPT-3 AI", guild_ids=[866199405090308116])
    async def openaiComplete(self, ctx, *, completion: Option(str, "The beginning of the sentence to complete", required=False)):
        async with aiohttp.ClientSession(json_serialize=ujson.dumps) as session:
            headers = {
                "Authorization": f"Bearer {OpenAI_API_KEY}",
                "Content-Type": "application/json",
            }
            payload = {
                "prompt": f"{completion}",
                "max_tokens": 16,
                "temperature": 0.35,
                "top_p": 0.20,
            }
            async with session.post(
                "https://api.openai.com/v1/engines/ada/completions",
                headers=headers,
                json=payload,
            ) as r:
                data = await r.json()
                try:
                    embedVar = discord.Embed()
                    embedVar.description = data["choices"][0]["text"]
                    await ctx.respond(embed=embedVar)
                except Exception as e:
                    embedVar = discord.Embed()
                    embedVar.description = "The query was not successful."
                    embedVar.add_field(name="Reason", value=e, inline=True)
                    await ctx.respond(embed=embedVar)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


class OpenAI2(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @slash_command(name="openai-classify", description="Classifies a sentence using OpenAI's GPT-3 AI", guild_ids=[866199405090308116])
    async def openaiClassify(self, ctx, *, query: Option(str, "The sentence to classify"), example1: Option(str, "The first example"), pos_or_neg1: Option(str, "Is the example above a negative example or positive example?", choices=["Positive", "Negative"]), example2: Option(str, "The second example"), pos_or_neg2: Option(str, "Is the example above a negative example or positive example?", choices=["Positive", "Negative"])):
        async with aiohttp.ClientSession(json_serialize=ujson.dumps) as session:
            headers = {
                "Authorization": f"Bearer {OpenAI_API_KEY}",
                "Content-Type": "application/json",
            }
            payload = {
                "query": f"{query}",
                "search_model": "curie",
                "model": "curie",
                "examples": [
                    [f"{example1}", f"{pos_or_neg1}"],
                    [f"{example2}", f"{pos_or_neg2}"],
                ],
            }
            async with session.post(
                "https://api.openai.com/v1/classifications",
                headers=headers,
                json=payload,
            ) as poster:
                data = await poster.json()
                try:
                    embedVar = discord.Embed()
                    for dictItem in data["selected_examples"]:
                        for keys, value in dictItem.items():
                            embedVar.add_field(name=keys, value=value, inline=True)
                    await ctx.respond(embed=embedVar)
                except Exception as e:
                    embedVar = discord.Embed()
                    embedVar.description = "The query was not successful."
                    embedVar.add_field(name="Reason", value=e, inline=True)
                    await ctx.respond(embed=embedVar)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


class OpenAI3(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(name="openai-answers", description="Forms an answer based on your question", guild_ids=[866199405090308116])
    async def openaiAnswers(self, ctx, *, question: Option(str, "The question to answer"), example_question: Option(str, "An example question to use as context"), example_answer: Option(str, "An example answer to use as context"), context: Option(str, "Some context for the answer you wrote")):
        async with aiohttp.ClientSession(json_serialize=ujson.dumps) as session:
            headers = {
                "Authorization": f"Bearer {OpenAI_API_KEY}",
                "Content-Type": "application/json",
            }
            payload = {
                "model": "ada",
                "question": question,
                "examples": [
                    [f"{example_question}", f"{example_answer}"]
                ],
                "examples_context": context,
                "documents": [],
            }
            async with session.post(
                "https://api.openai.com/v1/answers", headers=headers, json=payload
            ) as response:
                data = await response.json()
                try:
                    embedVar = discord.Embed()
                    embedVar.description = (
                        str(data["answers"])
                        .replace("[", "")
                        .replace("]", "")
                        .replace("'", "")
                    )
                    await ctx.respond(embed=embedVar)
                except Exception as e:
                    embedVar = discord.Embed()
                    embedVar.description = "The query was not successful."
                    embedVar.add_field(name="Reason", value=e, inline=True)
                    await ctx.respond(embed=embedVar)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())



def setup(bot):
    bot.add_cog(OpenAI1(bot))
    bot.add_cog(OpenAI2(bot))
    bot.add_cog(OpenAI3(bot))
