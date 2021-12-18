import aiohttp
import discord
import ujson
from discord.ext import commands
from discord_components import Button, Select, SelectOption
from dotenv import load_dotenv
from reactionmenu import ReactionMenu, Button, ButtonType
from pygicord import Paginator, control

load_dotenv()

def get_pages():
    pages = []
    for i in range(1, 6):
        embed = discord.Embed()
        embed.title = f"Embed no. {i}"
        pages.append(embed)
    return pages



class MangaDexV1(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="mangadex-search", aliases=["md-search"])
    async def manga(self, ctx, *, manga: str):
        async with aiohttp.ClientSession(json_serialize=ujson.dumps) as session:
            try:
                async with session.get(
                    f"https://api.mangadex.org/manga/?title={manga}&publicationDemographic[]=none&contentRating[]=safe&order[title]=asc"
                ) as r:
                    data = await r.json()
                    id = data["data"][0]["id"]
                    async with session.get(
                        f'https://api.mangadex.org/manga/{id}?includes["cover_art"]&contentRating["safe"]&order[title]=asc'
                    ) as resp:
                        md_data = await resp.json()
                        cover_art_id = md_data["data"]["relationships"][2]["id"]
                        async with session.get(
                            f"https://api.mangadex.org/cover/{cover_art_id}"
                        ) as rp:
                            cover_art_data = await rp.json()
                            cover_art = cover_art_data["data"]["attributes"]["fileName"]
                            if (
                                "en" in md_data["data"]["attributes"]["description"]
                                and md_data["data"]["attributes"]["title"]
                            ):
                                embedVar = discord.Embed()
                                embedVar.add_field(
                                    name="Title",
                                    value=md_data["data"]["attributes"]["title"]["en"],
                                    inline=True,
                                )
                                embedVar.add_field(
                                    name="Description (English)",
                                    value=str(
                                        md_data["data"]["attributes"]["description"][
                                            "en"
                                        ]
                                    )
                                    .replace("\n", "")
                                    .replace("\r", "")
                                    .replace("'", ""),
                                    inline=False,
                                )
                                embedVar.add_field(
                                    name="Publication Demographics",
                                    value=md_data["data"]["attributes"][
                                        "publicationDemographic"
                                    ],
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
                                            md_data["data"]["attributes"]["tags"][
                                                "attributes"
                                            ]["name"]["en"]
                                        )
                                        .replace("\n", "")
                                        .replace("'", "")
                                        for md_data["data"]["attributes"][
                                            "tags"
                                        ] in md_data["data"]["attributes"]["tags"]
                                    ],
                                    inline=True,
                                )
                                embedVar.set_image(
                                    url=f"https://uploads.mangadex.org/covers/{id}/{cover_art}"
                                )
                                await ctx.send(embed=embedVar)
                            elif (
                                "ja" in md_data["data"]["attributes"]["description"]
                                and md_data["data"]["attributes"]["title"]
                            ):
                                await ctx.send("prob using jpn desc")
                            elif (
                                None in md_data["data"]["attributes"]["description"]
                                and md_data["data"]["attributes"]["title"]
                            ):
                                await ctx.send("nope")
            except Exception as e:
                embedVar = discord.Embed()
                embedVar.description = (
                    "Sadly this command didn't work. Please try again"
                )
                embedVar.add_field(name="Reason", value=e, inline=True)
                await ctx.send(embed=embedVar)

    @manga.error
    async def on_message_error(
        self, ctx: commands.Context, error: commands.CommandError
    ):
        if isinstance(error, commands.MissingRequiredArgument):
            embedVar = discord.Embed(color=discord.Color.from_rgb(255, 51, 51))
            embedVar.description = f"Missing a required argument: {error.param}"
            msg = await ctx.send(embed=embedVar, delete_after=10)
            await msg.delete(delay=10)


class MangaDexV2(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="mangadex-random", aliases=["md-random"])
    async def manga_random(self, ctx):
        try:
            async with aiohttp.ClientSession(json_serialize=ujson.dumps) as session:
                async with session.get("https://api.mangadex.org/manga/random") as r:
                    data = await r.json()
                    id = data["data"]["id"]
                    cover_art_id = data["data"]["relationships"][2]["id"]
                    async with session.get(
                        f"https://api.mangadex.org/cover/{cover_art_id}"
                    ) as rp:
                        cover_art_data = await rp.json()
                        cover_art = cover_art_data["data"]["attributes"]["fileName"]
                        embedVar = discord.Embed(
                            title=data["data"]["attributes"]["title"]["en"]
                        )
                        embedVar.add_field(
                            name="Description",
                            value=[
                                str(
                                    data["data"]["attributes"]["description"]["en"]
                                ).replace("\n", "")
                            ],
                            inline=False,
                        )
                        embedVar.add_field(
                            name="Original Language",
                            value=data["data"]["attributes"]["originalLanguage"],
                            inline=True,
                        )
                        embedVar.add_field(
                            name="Last Volume",
                            value=[data["data"]["attributes"]["lastVolume"]],
                            inline=True,
                        )
                        embedVar.add_field(
                            name="Last Chapter",
                            value=[data["data"]["attributes"]["lastChapter"]],
                            inline=True,
                        )
                        embedVar.add_field(
                            name="Publication Demographic",
                            value=data["data"]["attributes"]["publicationDemographic"],
                            inline=True,
                        )
                        embedVar.add_field(
                            name="Status",
                            value=data["data"]["attributes"]["status"],
                            inline=True,
                        )
                        embedVar.add_field(
                            name="Content Rating",
                            value=data["data"]["attributes"]["contentRating"],
                            inline=True,
                        )

                        embedVar.set_image(
                            url=f"https://uploads.mangadex.org/covers/{id}/{cover_art}"
                        )
                        await ctx.send(embed=embedVar)
        except Exception as e:
            embedVar = discord.Embed()
            embedVar.description = (
                f"The query could not be performed. Please try again."
            )
            embedVar.add_field(name="Reason", value=e, inline=True)
            await ctx.send(embed=embedVar)


class MangaDexReaderV1(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Later this should allow for the name to be inputted, but for now it purely relies on the chapter id
    @commands.command(name="mangadex-read", aliases=["md-read"])
    async def manga_read(self, ctx, *, id: str):
        try:
            async with aiohttp.ClientSession(json_serialize=ujson.dumps) as session:
                async with session.get(f"https://api.mangadex.org/chapter/{id}") as r:
                    data = await r.json()
                    chapter_hash = data["data"]["attributes"]["hash"]
                    var = 0
                    var += 1
                    list_of_images = data["data"]["attributes"]["data"][var]
                    length_of_chapter = len(data["data"]["attributes"]["data"])
                    chapter_name = data["data"]["attributes"]["title"]
                    chapter_num = data["data"]["attributes"]["chapter"]
                    manga_id = data["data"]["relationships"][1]["id"]
                    async with session.get(
                        f"https://api.mangadex.org/manga/{manga_id}"
                    ) as resp:
                        data1 = await resp.json()
                        title = data1["data"]["attributes"]["title"]["en"]
                        embedVar = discord.Embed(
                            title=f"{title}",
                            color=discord.Color.from_rgb(231, 173, 255),
                        )
                        embedVar.description = f"{chapter_name} - Chapter {chapter_num}"
                        embedVar.set_image(
                            url=f"https://uploads.mangadex.org/data/{chapter_hash}/{list_of_images}"
                        )
                        await ctx.send(
                            embed=embedVar,
                            components=[
                                [
                                    Button(label="Go Back", style=1,
                                           custom_id="back"),
                                    Button(
                                        label=f"Page /{length_of_chapter}",
                                        style=2,
                                        custom_id="current_page",
                                        disabled=True,
                                    ),
                                    Button(
                                        label="Go Forwards",
                                        style=1,
                                        custom_id="forward",
                                    ),
                                ]
                            ],
                        )
                        interaction = await self.bot.wait_for(
                            "button_click", check=lambda i: i.custom_id == "back"
                        )
                        await interaction.ctx.send(
                            "Button is clicked", ephemeral="False"
                        )

        except Exception as e:
            await ctx.send(e)


class CustomPaginator(Paginator):
    @control(emoji="\N{INFORMATION SOURCE}", position=4.5)
    async def show_info(self, payload):
        """Shows this message."""
        desc = []
        for emoji, control_ in self.controller.items():
            desc.append(f"{emoji}: {control_.callback.__doc__}")
        embed = discord.Embed()
        embed.description = "\n".join(desc)
        embed.set_footer(text="Press any reaction to go back.")
        await self.message.edit(content=None, embed=embed)


pages = [f"Page no. {i}" for i in range(1, 6)]

class discordButtonTest(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name="button-test")
    async def user(self, ctx):
        paginator = CustomPaginator(pages=pages)
        await paginator.start(ctx)
        



def setup(bot):
    bot.add_cog(MangaDexV1(bot))
    bot.add_cog(MangaDexV2(bot))
    bot.add_cog(MangaDexReaderV1(bot))
    bot.add_cog(discordButtonTest(bot))
