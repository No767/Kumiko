import discord
import requests
import ujson
from discord.ext import commands


def get_anime_info(search):
    search = search.replace(" ", "%20")
    link = f"https://api.jikan.moe/v3/search/anime?q={search}"
    r = requests.get(link)
    anime_info = ujson.loads(r.text)
    return anime_info


def get_related_anime_info_pictures(id):
    link = f"https://api.jikan.moe/v3/anime/{id}/pictures"
    r = requests.get(link)
    return ujson.loads(r.text)


def get_anime_infov2(id):
    link = f"https://api.jikan.moe/v3/anime/{id}"
    r = requests.get(link)
    anime_info_v2 = ujson.loads(r.text)
    return anime_info_v2


class JikanV1(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="jikan-search")
    async def anime(self, ctx, *, search: str):
        anime_info = get_anime_info(search)
        id = anime_info["results"][0]["mal_id"]
        anime_info_v2 = get_anime_infov2(id)
        try:
            embedVar = discord.Embed(title=anime_info_v2["title"])
            embedVar.add_field(
                name="English Title", value=anime_info_v2["title_english"], inline=False
            )
            embedVar.add_field(
                name="Japanese Title",
                value=anime_info_v2["title_japanese"],
                inline=False,
            )
            embedVar.add_field(
                name="Title Synonyms",
                value=str(anime_info_v2["title_synonyms"])
                .replace("[", "")
                .replace("]", "")
                .replace("'", ""),
                inline=False,
            )
            embedVar.add_field(
                name="Synopsis",
                value=str(anime_info_v2["synopsis"]).replace(
                    "[Written by MAL Rewrite]", ""
                ),
                inline=False,
            )
            embedVar.add_field(
                name="Background", value=anime_info_v2["background"], inline=False
            )
            embedVar.add_field(
                name="Type", value=anime_info_v2["type"], inline=False)
            embedVar.add_field(
                name="Source", value=anime_info_v2["source"], inline=False
            )
            embedVar.add_field(
                name="Status", value=anime_info_v2["status"], inline=False
            )
            embedVar.add_field(
                name="Aired", value=anime_info_v2["aired"]["string"], inline=False
            )
            embedVar.add_field(
                name="Premiered", value=anime_info_v2["premiered"], inline=False
            )
            embedVar.add_field(
                name="Rating", value=anime_info_v2["rating"], inline=False
            )
            embedVar.add_field(
                name="Score", value=anime_info_v2["score"], inline=False)
            embedVar.add_field(
                name="Scored By", value=anime_info_v2["scored_by"], inline=False
            )
            embedVar.add_field(
                name="Rank", value=anime_info_v2["rank"], inline=False)
            embedVar.add_field(
                name="Popularity", value=anime_info_v2["popularity"], inline=False
            )
            embedVar.add_field(
                name="Members", value=anime_info_v2["members"], inline=False
            )
            embedVar.add_field(
                name="Favorites", value=anime_info_v2["favorites"], inline=False
            )
            embedVar.set_thumbnail(url=anime_info_v2["image_url"])
            await ctx.send(embed=embedVar)
        except Exception as e:
            embedVar = discord.Embed()
            embedVar.description = (
                f"The query could not be performed. Please try again.\nReason: {e}"
            )
            await ctx.send(embed=embedVar)


def setup(bot):
    bot.add_cog(JikanV1(bot))
