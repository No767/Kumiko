
import aiohttp
import discord
import ujson
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()


class MangadexV1(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.session = aiohttp.ClientSession(json_serialize=ujson.dumps)

    @commands.command(name="mangadex-search", aliases=["md-search"])
    async def manga(self, ctx, *, manga: str):
        params = {"title": f"{manga}"}
        async with self.session.get(
            f"https://api.mangadex.org/manga/", params=params
        ) as r:
            data = await r.json()
            id = data["data"][0]["id"]
            async with self.session.get(
                f'https://api.mangadex.org/manga/{id}?includes["cover_art"]'
            ) as resp:
                md_data = await resp.json()
                cover_art_id = md_data["data"]["relationships"][2]["id"]
                embedVar = discord.Embed(
                    title=md_data["data"]["attributes"]["title"]["en"]
                )
                embedVar.add_field(
                    name="Alt Title",
                    value=md_data["data"]["attributes"]["altTitles"]["en"],
                    inline=True,
                )
                embedVar.add_field(
                    name="Japanese Title",
                    value=md_data["data"]["attributes"]["altTitles"]["ja"],
                    inline=True,
                )
                embedVar.add_field(
                    name="Description",
                    value=str(md_data["data"]["attributes"]
                              ["description"]["en"])
                    .replace("\n", "")
                    .replace("\r", ""),
                    inline=False,
                )
                embedVar.add_field(
                    name="MAL ID",
                    value=md_data["data"]["attributes"]["links"]["mal_id"],
                    inline=True,
                )
                embedVar.add_field(
                    name="Original Language",
                    value=md_data["data"]["attributes"]["originalLanguage"],
                    inline=True,
                )
                embedVar.add_field(
                    name="Last Volume",
                    value=md_data["data"]["attributes"]["lastVolume"],
                    inline=True,
                )
                embedVar.add_field(
                    name="Last Chapter",
                    value=md_data["data"]["attributes"]["lastChapter"],
                    inline=True,
                )
                embedVar.add_field(
                    name="Publication Demographics",
                    value=md_data["data"]["attributes"]["publicationDemographics"],
                    inline=True,
                )
                embedVar.add_field(
                    name="Status",
                    value=md_data["data"]["attributes"]["status"],
                    inline=True,
                )
                embedVar.add_field(
                    name="Year",
                    value=md_data["data"]["attributes"]["year"],
                    inline=True,
                )
                embedVar.add_field(
                    name="Tags",
                    value=[
                        str(
                            md_data["data"]["attributes"]["tags"]["attributes"]["name"][
                                "en"
                            ]
                        ).replace("\n", "")
                        for md_data["data"]["attributes"]["tags"] in md_data["data"][
                            "attributes"
                        ]["tags"]
                    ],
                    inline=True,
                )
                embedVar.set_thumbnail(
                    url=f"https://uploads.mangadex.org/covers/{id}/{cover_art_id}.jpg"
                )  # this part is currently not working
                await ctx.send(embed=embedVar)
