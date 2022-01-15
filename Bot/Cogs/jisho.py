import re

import discord
import orjson
import aiohttp
from discord.ext import commands
from jamdict import Jamdict
import asyncio
import uvloop

jam = Jamdict()

def kanjiv2(search):
    res = jam.lookup(search.replace("\n", " "))
    for c in res.chars:
        return str(c).replace("\n", " ")


def hiragana(search):
    result = jam.lookup(search)
    for word in result.entries:
        m = re.findall("[ぁ-ん]", str(word))
        r = str(m).replace("'", "").replace(",", "").replace(" ", "")
        return str(r)


def katakana(search):
    result = jam.lookup(search.replace("\n", " "))
    for entry in result.entries:
        m = re.findall("[ァ-ン]", str(entry))
        r = (
            str(m)
            .replace("[", " ")
            .replace("]", " ")
            .replace("'", " ")
            .replace(",", "")
            .replace(" ", "")
        )
        return str(r)


def searcher(search):
    result = jam.lookup(search)
    for word in result.entries:
        return str(word[4:10])


def better_hiragana(search):
    searcher(search)


class jisho_dict(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="jisho")
    async def jisho(self, ctx, search: str):
        async with aiohttp.ClientSession(json_serialize=orjson.dumps) as session:
            params = {"keyword": search}
            async with session.get("https://jisho.org/api/v1/search/words", params=params) as r:
                jisho = await r.json()
                try:
                    res = jam.lookup(search)
                    embedVar = discord.Embed()
                    embedVar.add_field(
                        name="Kanji",
                        value=[str(c).replace("'", "") for c in res.chars],
                        inline=False,
                    )
                    embedVar.add_field(
                        name="Position of Speech (POS)", value=jisho["data"][0]["senses"][0]["parts_of_speech"], inline=False
                    )
                    embedVar.add_field(name="Is Common?", value=jisho["data"][0]["is_common"], inline=False)
                    embedVar.add_field(
                        name="Other Info",
                        value=f"Tags >> {jisho['data'][0]['tags']}\nJLPT >> {jisho['data'][0]['tags']}\nAntonyms >> {jisho['data'][0]['senses'][0]['antonyms']}\nSee Also >> {jisho['data'][0]['senses'][0]['see_also']}\nLinks >> {jisho['data'][0]['senses'][0]['links']}",
                        inline=False,
                    )
                    embedVar.add_field(
                        name="Attributions",
                        value=f"JMDict >> {jisho['data'][0]['attribution']['jmdict']}\nJMNEDict >> {jisho['data'][0]['attribution']['jmnedict']}\nDBPedia >> {jisho['data'][0]['attribution']['dbpedia']}",
                        inline=False,
                    )
                    embedVar.add_field(
                        name="HTTP Status (Jisho API)",
                        value=f"{jisho['meta']['status']}",
                        inline=False,
                    )
                    embedVar.description = str([str(word[0])
                                               for word in res.entries])
                    await ctx.send(embed=embedVar)
                except Exception as e:
                    embed_discord = discord.Embed()
                    embed_discord.description = (
                        f"An error has occurred. Please try again\nReason: {e}"
                    )
                    await ctx.send(embed=embed_discord)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    @jisho.error
    async def on_message_error(
        self, ctx: commands.Context, error: commands.CommandError
    ):
        if isinstance(error, commands.MissingRequiredArgument):
            embed_discord = discord.Embed()
            embed_discord.description = f"Missing a requireed argument: {error.param}"
            await ctx.send(embed=embed_discord)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


def setup(bot):
    bot.add_cog(jisho_dict(bot))
