import re

import discord
import requests
import ujson
from discord.ext import commands
from dotenv import load_dotenv
from jamdict import Jamdict

load_dotenv()
jam = Jamdict()

# Use Array Loop Instead


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


# old kanji lookup system. use the function kanjiv2 instead
def kanji(search):
    result = jam.lookup(search)
    result_search = result.text(separator=" | ", with_chars=False, no_id=True)
    m = re.findall(".[一-龯]", result_search)
    all_kanji = str(m).replace(",", "")[1:-1]
    all_kanjiv2 = all_kanji.replace("'", "").replace(" ", "").replace("", ", ")
    return all_kanjiv2


def english_def_part2(search):
    result = jam.lookup(search.replace(" ", "\n"))
    return (
        str(result.chars)
        .replace("[", " ")
        .replace("]", " ")
        .replace(",", ", ")
        .replace(":", " ")
    )


def tag(search):
    search = search.replace(" ", "%20")
    link = f"https://jisho.org/api/v1/search/words?keyword={search}"
    r = requests.get(link)
    jisho = ujson.loads(r.text)
    jisho_tag = str(jisho["data"][0]["tags"])
    return jisho_tag.replace("[", " ").replace("]", " ").replace("'", " ")


def jlpt(search):
    search = search.replace(" ", "%20")
    link = f"https://jisho.org/api/v1/search/words?keyword={search}"
    r = requests.get(link)
    jisho = ujson.loads(r.text)
    jisho_jlpt = str(jisho["data"][0]["tags"])
    return jisho_jlpt.replace("[", " ").replace("]", " ").replace("'", " ")


def is_common(search):
    search = search.replace(" ", "%20")
    link = f"https://jisho.org/api/v1/search/words?keyword={search}"
    r = requests.get(link)
    jisho = ujson.loads(r.text)
    jishov1 = str(jisho["data"][0]["is_common"])
    return jishov1.replace("[", " ").replace("]", " ")


def pos(search):
    search = search.replace(" ", "%20")
    link = f"https://jisho.org/api/v1/search/words?keyword={search}"
    r = requests.get(link)
    jisho = ujson.loads(r.text)
    jisho_sorted = jisho["data"][0]["senses"][0]["parts_of_speech"]
    return str(jisho_sorted).replace("[", "").replace("]", "").replace("'", "")


def see_also(search):
    search = search.replace(" ", "%20")
    link = f"https://jisho.org/api/v1/search/words?keyword={search}"
    r = requests.get(link)
    jisho = ujson.loads(r.text)
    jisho_sorted = jisho["data"][0]["senses"][0]["see_also"]
    return str(jisho_sorted).replace("[", "").replace("]", "").replace("'", "")


def antonyms(search):
    search = search.replace(" ", "%20")
    link = f"https://jisho.org/api/v1/search/words?keyword={search}"
    r = requests.get(link)
    jisho = ujson.loads(r.text)
    jisho_sorted = jisho["data"][0]["senses"][0]["antonyms"]
    return str(jisho_sorted).replace("[", "").replace("]", "").replace("'", "")


def links(search):
    search = search.replace(" ", "%20")
    link = f"https://jisho.org/api/v1/search/words?keyword={search}"
    r = requests.get(link)
    jisho = ujson.loads(r.text)
    jisho_sorted = jisho["data"][0]["senses"][0]["links"]
    return str(jisho_sorted).replace("[", "").replace("]", "").replace("'", "")


class jisho_dict(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="jisho")
    async def jisho(self, ctx, search: str):
        try:
            result = jam.lookup(search)
            link = f"https://jisho.org/api/v1/search/words?keyword={search}"
            r = requests.get(link)
            jisho = ujson.loads(r.text)
            res = jam.lookup(search.replace("\n", " "))
            embedVar = discord.Embed()
            embedVar.add_field(name="Kanji", value=[str(c).replace("'", "") for c in res.chars], inline=False)
            embedVar.add_field(name="Hiragana", value=[str(re.findall('[ぁ-ん]', str(word))).replace('"', '').replace(", ", "").replace("'", "") for word in result.entries], inline=False)
            embedVar.add_field(name="Katanana", value=[str(re.findall("[ァ-ン]", str(entry))).replace('"', '').replace(", ", "").replace("'", "") for entry in result.entries], inline=False)
            embedVar.add_field(name="Position of Speech (POS)", value=pos(search), inline=False)
            embedVar.add_field(
                name="English Defintion(s)",
                value=english_def_part2(search),
                inline=False,
            )
            embedVar.add_field(name="Is Common?",
                               value=is_common(search), inline=False)
            embedVar.add_field(
                name="Other Info",
                value=f"Tags >> {tag(search)}\nJLPT >> {jlpt(search)}\nAntonyms >> {antonyms(search)}\nSee Also >> {see_also(search)}\nLinks >> {links(search)}",
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
            await ctx.send(embed=embedVar)
        except Exception as e:
            embed_discord = discord.Embed()
            embed_discord.description = (
                f"An error has occurred. Please try again\nReason: {e}"
            )
            await ctx.send(embed=embed_discord)

    @jisho.error
    async def on_message_error(
        self, ctx: commands.Context, error: commands.CommandError
    ):
        if isinstance(error, commands.MissingRequiredArgument):
            embed_discord = discord.Embed()
            embed_discord.description = f"Missing a requireed argument: {error.param}"
            await ctx.send(embed=embed_discord)


def setup(bot):
    bot.add_cog(jisho_dict(bot))
