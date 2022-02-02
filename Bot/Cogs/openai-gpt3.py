import asyncio
import os

import aiohttp
import discord
import ujson
import uvloop
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

OpenAI_API_KEY = os.getenv("OpenAI_API_Key")


class OpenAI1(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="openai-complete", aliases=["ai-complete"])
    async def openaiComplete(self, ctx, *, completion=None):
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
                    await ctx.send(embed=embedVar)
                except Exception as e:
                    embedVar = discord.Embed()
                    embedVar.description = "The query was not successful."
                    embedVar.add_field(name="Reason", value=e, inline=True)
                    await ctx.send(embed=embedVar)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    @openaiComplete.error
    async def on_message_error(
        self, ctx: commands.Context, error: commands.CommandError
    ):
        if isinstance(error, commands.MissingRequiredArgument):
            embedVar = discord.Embed(color=discord.Color.from_rgb(255, 51, 51))
            embedVar.description = f"Missing a requireed argument: {error.param}"
            msg = await ctx.send(embed=embedVar, delete_after=10)
            await msg.delete(delay=10)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


class OpenAI2(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="openai-classify", aliases=["ai-classify"])
    async def openaiClassify(self, ctx):
        def check(ms):
            return ms.channel == ctx.message.channel and ms.author == ctx.message.author

        await ctx.send("Enter in query here:")
        query1 = await self.bot.wait_for("message", check=check)
        await ctx.send("Enter in an example in order to get classify:")
        searchTerm1 = await self.bot.wait_for("message", check=check)
        await ctx.send(
            "Is the example above a negative example or positive example? (For example, I am sad would be considered negative):"
        )
        posOrNegExample1 = await self.bot.wait_for("message", check=check)
        await ctx.send("Enter in another example:")
        searchTerm2 = await self.bot.wait_for("message", check=check)
        await ctx.send("Is the example above a negative example or positive example?:")
        posOrNegExample2 = await self.bot.wait_for("message", check=check)
        async with aiohttp.ClientSession(json_serialize=ujson.dumps) as session:
            headers = {
                "Authorization": f"Bearer {OpenAI_API_KEY}",
                "Content-Type": "application/json",
            }
            payload = {
                "query": f"{query1.content}",
                "search_model": "curie",
                "model": "curie",
                "examples": [
                    [f"{searchTerm1.content}", f"{posOrNegExample1.content}"],
                    [f"{searchTerm2.content}", f"{posOrNegExample2.content}"],
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
                    embedVar.add_field(
                        name="Label (Query)", value=data["label"], inline=True
                    )
                    embedVar.add_field(
                        name="Label",
                        value=data["selected_examples"][0]["label"],
                        inline=True,
                    )
                    embedVar.add_field(
                        name="Text",
                        value=data["selected_examples"][0]["text"],
                        inline=True,
                    )
                    embedVar.add_field(
                        name="Label",
                        value=data["selected_examples"][1]["label"],
                        inline=True,
                    )
                    embedVar.add_field(
                        name="Text",
                        value=data["selected_examples"][1]["text"],
                        inline=True,
                    )
                    await ctx.send(embed=embedVar)
                except Exception as e:
                    embedVar = discord.Embed()
                    embedVar.description = "The query was not successful."
                    embedVar.add_field(name="Reason", value=e, inline=True)
                    await ctx.send(embed=embedVar)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    @openaiClassify.error
    async def on_message_error(
        self, ctx: commands.Context, error: commands.CommandError
    ):
        if isinstance(error, commands.MissingRequiredArgument):
            embedVar = discord.Embed(color=discord.Color.from_rgb(255, 51, 51))
            embedVar.description = f"Missing a requireed argument: {error.param}"
            msg = await ctx.send(embed=embedVar, delete_after=10)
            await msg.delete(delay=10)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


class OpenAI3(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="openai-answers", aliases=["ai-answers"])
    async def openaiAnswers(self, ctx):
        def check(ms):
            return ms.channel == ctx.message.channel and ms.author == ctx.message.author

        await ctx.send("Enter in question here:")
        question1 = await self.bot.wait_for("message", check=check)
        await ctx.send("Enter in an example question:")
        exampleQuestion = await self.bot.wait_for("message", check=check)
        await ctx.send("Enter the answer for the question you just sent:")
        exampleAnswer = await self.bot.wait_for("message", check=check)
        await ctx.send("Enter in some context for the questions you just wrote:")
        context = await self.bot.wait_for("message", check=check)
        async with aiohttp.ClientSession(json_serialize=ujson.dumps) as session:
            headers = {
                "Authorization": f"Bearer {OpenAI_API_KEY}",
                "Content-Type": "application/json",
            }
            payload = {
                "model": "ada",
                "question": question1.content,
                "examples": [
                    [f"{exampleQuestion.content}", f"{exampleAnswer.content}"]
                ],
                "examples_context": context.content,
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
                    await ctx.send(embed=embedVar)
                except Exception as e:
                    embedVar = discord.Embed()
                    embedVar.description = "The query was not successful."
                    embedVar.add_field(name="Reason", value=e, inline=True)
                    await ctx.send(embed=embedVar)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    @openaiAnswers.error
    async def on_message_error(
        self, ctx: commands.Context, error: commands.CommandError
    ):
        if isinstance(error, commands.MissingRequiredArgument):
            embedVar = discord.Embed(color=discord.Color.from_rgb(255, 51, 51))
            embedVar.description = f"Missing a requireed argument: {error.param}"
            msg = await ctx.send(embed=embedVar, delete_after=10)
            await msg.delete(delay=10)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


def setup(bot):
    bot.add_cog(OpenAI1(bot))
    bot.add_cog(OpenAI2(bot))
    bot.add_cog(OpenAI3(bot))
