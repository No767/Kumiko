import aiohttp
import discord
import ujson
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()


class MangaDexV1(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="mangadex-search", aliases=["md-search"])
    async def manga(self, ctx, *, manga: str):
        async with aiohttp.ClientSession(json_serialize=ujson.dumps) as session:
            try:
                
                params = {"title": f"{manga}"}
                async with session.get(
                    f"https://api.mangadex.org/manga/", params=params
                ) as r:
                    data = await r.json()
                    id = data["data"][0]["id"]
                    async with session.get(
                        f'https://api.mangadex.org/manga/{id}?includes["cover_art"]&contentRating["safe"]'
                    ) as resp:
                        md_data = await resp.json()
                        cover_art_id = md_data["data"]["relationships"][2]["id"]
                        async with session.get(f"https://api.mangadex.org/cover/{cover_art_id}") as rp:
                            cover_art_data = await rp.json()
                            cover_art = cover_art_data["data"]["attributes"]["fileName"]
                            embedVar = discord.Embed()
                            embedVar.add_field(name="Title", value=md_data["data"]["attributes"]["title"], inline=True)
                            embedVar.add_field(
                                name="Description",
                                value=str(md_data["data"]["attributes"]
                                          ["description"])
                                .replace("\n", "")
                                .replace("\r", ""),
                                inline=False,
                            )
                            embedVar.add_field(
                                name="Publication Demographics",
                                value=md_data["data"]["attributes"]["publicationDemographic"],
                                inline=True,
                            )
                            embedVar.add_field(
                                name="Status",
                                value=md_data["data"]["attributes"]["status"],
                                inline=True,
                            )
                            embedVar.add_field(
                                name="Tags",
                                value=[
                                    str(
                                        md_data["data"]["attributes"]["tags"]["attributes"]["name"][
                                            "en"
                                        ]
                                    ).replace("\n", "").replace("'", "")
                                    for md_data["data"]["attributes"]["tags"] in md_data["data"][
                                        "attributes"
                                    ]["tags"]
                                ],
                                inline=True,
                            )
                            embedVar.set_image(
                                url=f"https://uploads.mangadex.org/covers/{id}/{cover_art}"
                            ) 
                            await ctx.send(embed=embedVar)
            except Exception as e:
                await ctx.send(e)
    @manga.error
    async def on_message_error(
        self, ctx: commands.Context, error: commands.CommandError
    ):
        if isinstance(error, commands.MissingRequiredArgument):
            embedVar = discord.Embed(color=discord.Color.from_rgb(255, 51, 51))
            embedVar.description = f"Missing a required argument: {error.param}"
            msg = await ctx.send(embed=embedVar, delete_after=10)
            await msg.delete(delay=10)

def setup(bot):
    bot.add_cog(MangaDexV1(bot))