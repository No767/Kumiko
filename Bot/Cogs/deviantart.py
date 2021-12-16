import discord
import requests
import ujson
from discord.ext import commands
from dotenv import load_dotenv
from sqlalchemy import Column, MetaData, String, Table, create_engine

load_dotenv()


def getTokens():
    meta = MetaData()
    engine = create_engine("sqlite:///daTokens/tokens.db")
    tokens = Table(
        "DA_Tokens",
        meta,
        Column("Access_Tokens", String),
        Column("Refresh_Tokens", String),
    )
    s = tokens.select()
    conn = engine.connect()
    result_select = conn.execute(s)
    for row in result_select:
        return row
    conn.close()


DeviantArt_API_Access_Token = getTokens()[0]


def get_deviation(deviation_id):
    link = f"https://www.deviantart.com/api/v1/oauth2/deviation/{deviation_id}?with_session=false&limit=5&access_token={DeviantArt_API_Access_Token}"
    r = requests.get(link)
    return ujson.loads(r.text)


def status_code_get_deviations(deviation_id):
    link = f"https://www.deviantart.com/api/v1/oauth2/deviation/{deviation_id}?with_session=false&limit=10&access_token={DeviantArt_API_Access_Token}"
    r = requests.get(link)
    return r.status_code


def get_newest(search):
    link = f"https://www.deviantart.com/api/v1/oauth2/browse/newest?q={search}&with_session=false&limit=10&mature_content=false&access_token={DeviantArt_API_Access_Token}"
    r = requests.get(link)
    return ujson.loads(r.text)


def get_popular(search):
    link = f"https://www.deviantart.com/api/v1/oauth2/browse/popular?q={search}&with_session=false&limit=10&mature_content=false&access_token={DeviantArt_API_Access_Token}"
    r = requests.get(link)
    return ujson.loads(r.text)


def get_tags(search):
    link = f"https://www.deviantart.com/api/v1/oauth2/browse/tags?tag={search}&with_session=false&limit=10&mature_content=false&access_token={DeviantArt_API_Access_Token}"
    r = requests.get(link)
    return ujson.loads(r.text)


def get_users(search):
    link = f"https://www.deviantart.com/api/v1/oauth2/user/profile/{search}?ext_collections=false&ext_galleries=false&with_session=false&mature_content=false&access_token={DeviantArt_API_Access_Token}"
    r = requests.get(link)
    return ujson.loads(r.text)


class DeviantArtV1(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="deviantart-item", aliases=["da-item"])
    async def da(self, ctx, *, deviation_id: str):
        deviation = get_deviation(deviation_id)
        try:
            if status_code_get_deviations(deviation_id) == 200:
                embedVar = discord.Embed(
                    title=deviation["title"],
                    color=discord.Color.from_rgb(255, 214, 214),
                )
                embedVar.add_field(
                    name="Creator", value=deviation["author"]["username"], inline=True
                )
                embedVar.add_field(
                    name="Category", value=deviation["category"], inline=True
                )
                embedVar.add_field(
                    name="Comments", value=deviation["stats"]["comments"], inline=True
                )
                embedVar.add_field(
                    name="Favorites",
                    value=deviation["stats"]["favourites"],
                    inline=True,
                )
                embedVar.add_field(
                    name="Is Mature", value=deviation["is_mature"], inline=True
                )
                embedVar.add_field(
                    name="URL", value=deviation["url"], inline=True)
                embedVar.set_image(url=deviation["content"]["src"])
                embedVar.set_thumbnail(url=deviation["author"]["usericon"])
                await ctx.send(embed=embedVar)
            else:
                embedVar = discord.Embed(
                    color=discord.Color.from_rgb(255, 214, 214))
                embedVar.description = "The query failed. Please try again"
                embedVar.add_field(
                    name="Error", value=deviation["error"], inline=True)
                embedVar.add_field(
                    name="Error Description",
                    value=deviation["error_description"],
                    inline=True,
                )
                embedVar.add_field(
                    name="Status", value=deviation["status"], inline=True
                )
                await ctx.send(embed=embedVar)
        except Exception as e:
            embedVar = discord.Embed(
                color=discord.Color.from_rgb(255, 214, 214))
            embedVar.description = "The query failed. Please try again"
            embedVar.add_field(name="Reason", value=e, inline=False)
            embedVar.add_field(
                name="Error", value=deviation["error"], inline=True)
            embedVar.add_field(
                name="Error Description",
                value=deviation["error_description"],
                inline=True,
            )
            embedVar.add_field(
                name="Status", value=deviation["status"], inline=True)
            await ctx.send(embed=embedVar)

    @da.error
    async def on_message_error(
        self, ctx: commands.Context, error: commands.CommandError
    ):
        if isinstance(error, commands.MissingRequiredArgument):
            embedVar = discord.Embed(color=discord.Color.from_rgb(255, 51, 51))
            embedVar.description = f"Missing a required argument: {error.param}"
            msg = await ctx.send(embed=embedVar, delete_after=10)
            await msg.delete(delay=10)


class DeviantArtV2(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="deviantart-newest", aliases=["da-newest"])
    async def da_query(self, ctx, *, search: str):
        search = search.replace(" ", "%20")
        art = get_newest(search)
        try:
            if int(art["estimated_total"]) > 5:
                embedVar1 = discord.Embed(
                    title=art["results"][0]["title"],
                    color=discord.Color.from_rgb(255, 156, 192),
                )
                embedVar1.add_field(
                    name="Creator",
                    value=art["results"][0]["author"]["username"],
                    inline=True,
                )
                embedVar1.add_field(
                    name="Category", value=art["results"][0]["category"], inline=True
                )
                embedVar1.add_field(
                    name="Comments",
                    value=art["results"][0]["stats"]["comments"],
                    inline=True,
                )
                embedVar1.add_field(
                    name="Favorites",
                    value=art["results"][0]["stats"]["favourites"],
                    inline=True,
                )
                embedVar1.add_field(
                    name="Deviation ID",
                    value=art["results"][0]["deviationid"],
                    inline=True,
                )
                embedVar1.add_field(
                    name="URL", value=art["results"][0]["url"], inline=True
                )
                embedVar1.set_image(url=art["results"][0]["content"]["src"])
                embedVar1.set_thumbnail(
                    url=art["results"][0]["author"]["usericon"])
                await ctx.send(embed=embedVar1)
                embedVar2 = discord.Embed(
                    title=art["results"][1]["title"],
                    color=discord.Color.from_rgb(219, 156, 255),
                )
                embedVar2.add_field(
                    name="Creator",
                    value=art["results"][1]["author"]["username"],
                    inline=True,
                )
                embedVar2.add_field(
                    name="Category", value=art["results"][1]["category"], inline=True
                )
                embedVar2.add_field(
                    name="Comments",
                    value=art["results"][1]["stats"]["comments"],
                    inline=True,
                )
                embedVar2.add_field(
                    name="Favorites",
                    value=art["results"][1]["stats"]["favourites"],
                    inline=True,
                )
                embedVar2.add_field(
                    name="Deviation ID",
                    value=art["results"][1]["deviationid"],
                    inline=True,
                )
                embedVar2.add_field(
                    name="URL", value=art["results"][1]["url"], inline=True
                )
                embedVar2.set_image(url=art["results"][1]["content"]["src"])
                embedVar2.set_thumbnail(
                    url=art["results"][1]["author"]["usericon"])
                await ctx.send(embed=embedVar2)
                embedVar3 = discord.Embed(
                    title=art["results"][2]["title"],
                    color=discord.Color.from_rgb(168, 156, 255),
                )
                embedVar3.add_field(
                    name="Creator",
                    value=art["results"][2]["author"]["username"],
                    inline=True,
                )
                embedVar3.add_field(
                    name="Category", value=art["results"][2]["category"], inline=True
                )
                embedVar3.add_field(
                    name="Comments",
                    value=art["results"][2]["stats"]["comments"],
                    inline=True,
                )
                embedVar3.add_field(
                    name="Favorites",
                    value=art["results"][2]["stats"]["favourites"],
                    inline=True,
                )
                embedVar3.add_field(
                    name="Deviation ID",
                    value=art["results"][2]["deviationid"],
                    inline=True,
                )
                embedVar3.add_field(
                    name="URL", value=art["results"][2]["url"], inline=True
                )
                embedVar3.set_image(url=art["results"][2]["content"]["src"])
                embedVar3.set_thumbnail(
                    url=art["results"][2]["author"]["usericon"])
                await ctx.send(embed=embedVar3)
                embedVar4 = discord.Embed(
                    title=art["results"][3]["title"],
                    color=discord.Color.from_rgb(156, 207, 255),
                )
                embedVar4.add_field(
                    name="Creator",
                    value=art["results"][3]["author"]["username"],
                    inline=True,
                )
                embedVar4.add_field(
                    name="Category", value=art["results"][3]["category"], inline=True
                )
                embedVar4.add_field(
                    name="Comments",
                    value=art["results"][3]["stats"]["comments"],
                    inline=True,
                )
                embedVar4.add_field(
                    name="Favorites",
                    value=art["results"][3]["stats"]["favourites"],
                    inline=True,
                )
                embedVar4.add_field(
                    name="Deviation ID",
                    value=art["results"][3]["deviationid"],
                    inline=True,
                )
                embedVar4.add_field(
                    name="URL", value=art["results"][3]["url"], inline=True
                )
                embedVar4.set_image(url=art["results"][3]["content"]["src"])
                embedVar4.set_thumbnail(
                    url=art["results"][3]["author"]["usericon"])
                await ctx.send(embed=embedVar4)
                embedVar5 = discord.Embed(
                    title=art["results"][4]["title"],
                    color=discord.Color.from_rgb(156, 255, 225),
                )
                embedVar5.add_field(
                    name="Creator",
                    value=art["results"][4]["author"]["username"],
                    inline=True,
                )
                embedVar5.add_field(
                    name="Category", value=art["results"][4]["category"], inline=True
                )
                embedVar5.add_field(
                    name="Comments",
                    value=art["results"][4]["stats"]["comments"],
                    inline=True,
                )
                embedVar5.add_field(
                    name="Favorites",
                    value=art["results"][4]["stats"]["favourites"],
                    inline=True,
                )
                embedVar5.add_field(
                    name="Deviation ID",
                    value=art["results"][4]["deviationid"],
                    inline=True,
                )
                embedVar5.add_field(
                    name="URL", value=art["results"][4]["url"], inline=True
                )
                embedVar5.set_image(url=art["results"][4]["content"]["src"])
                embedVar5.set_thumbnail(
                    url=art["results"][4]["author"]["usericon"])
                await ctx.send(embed=embedVar5)
            else:
                embedVar = discord.Embed(
                    color=discord.Color.from_rgb(255, 156, 192))
                embedVar.add_field(
                    name="Has More", value=art["has_more"], inline=True)
                embedVar.add_field(
                    name="Estimated Total", value=art["estimated_total"], inline=True
                )
                embedVar.add_field(name="Total", value=len(
                    art["results"]), inline=True)
                embedVar.set_footer(
                    text="This only appears if the estimated total is less than 5 results. Info given here are for reference."
                )
                await ctx.send(embed=embedVar)
        except Exception as e:
            embedVar = discord.Embed(
                color=discord.Color.from_rgb(255, 214, 214))
            embedVar.description = "The query failed. Please try again"
            embedVar.add_field(name="Reason", value=e, inline=False)
            embedVar.add_field(name="Error", value=art["error"], inline=True)
            embedVar.add_field(
                name="Error Description", value=art["error_description"], inline=True
            )
            embedVar.add_field(name="Status", value=art["status"], inline=True)
            await ctx.send(embed=embedVar)

    @da_query.error
    async def on_message_error(
        self, ctx: commands.Context, error: commands.CommandError
    ):
        if isinstance(error, commands.MissingRequiredArgument):
            embedVar = discord.Embed(color=discord.Color.from_rgb(255, 51, 51))
            embedVar.description = f"Missing a required argument: {error.param}"
            msg = await ctx.send(embed=embedVar, delete_after=10)
            await msg.delete(delay=10)


class DeviantArtV3(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="deviantart-popular", aliases=["da-popular"])
    async def deviantart_popular(self, ctx, *, search: str):
        search = search.replace(" ", "%20")
        pop = get_popular(search)
        try:
            if pop["estimated_total"] > 5:
                embedVar1 = discord.Embed(
                    title=pop["results"][0]["title"],
                    color=discord.Color.from_rgb(255, 250, 181),
                )
                embedVar1.add_field(
                    name="Creator",
                    value=pop["results"][0]["author"]["username"],
                    inline=True,
                )
                embedVar1.add_field(
                    name="Category", value=pop["results"][0]["category"], inline=True
                )
                embedVar1.add_field(
                    name="Comments",
                    value=pop["results"][0]["stats"]["comments"],
                    inline=True,
                )
                embedVar1.add_field(
                    name="Favorites",
                    value=pop["results"][0]["stats"]["favourites"],
                    inline=True,
                )
                embedVar1.add_field(
                    name="Deviation ID",
                    value=pop["results"][0]["deviationid"],
                    inline=True,
                )
                embedVar1.add_field(
                    name="URL", value=pop["results"][0]["url"], inline=True
                )
                embedVar1.set_image(url=pop["results"][0]["content"]["src"])
                embedVar1.set_thumbnail(
                    url=pop["results"][0]["author"]["usericon"])
                await ctx.send(embed=embedVar1)
                embedVar2 = discord.Embed(
                    title=pop["results"][1]["title"],
                    color=discord.Color.from_rgb(255, 250, 181),
                )
                embedVar2.add_field(
                    name="Creator",
                    value=pop["results"][1]["author"]["username"],
                    inline=True,
                )
                embedVar2.add_field(
                    name="Category", value=pop["results"][1]["category"], inline=True
                )
                embedVar2.add_field(
                    name="Comments",
                    value=pop["results"][1]["stats"]["comments"],
                    inline=True,
                )
                embedVar2.add_field(
                    name="Favorites",
                    value=pop["results"][1]["stats"]["favourites"],
                    inline=True,
                )
                embedVar2.add_field(
                    name="Deviation ID",
                    value=pop["results"][1]["deviationid"],
                    inline=True,
                )
                embedVar2.add_field(
                    name="URL", value=pop["results"][1]["url"], inline=True
                )
                embedVar2.set_image(url=pop["results"][1]["content"]["src"])
                embedVar2.set_thumbnail(
                    url=pop["results"][1]["author"]["usericon"])
                await ctx.send(embed=embedVar2)
                embedVar3 = discord.Embed(
                    title=pop["results"][2]["title"],
                    color=discord.Color.from_rgb(255, 250, 181),
                )
                embedVar3.add_field(
                    name="Creator",
                    value=pop["results"][2]["author"]["username"],
                    inline=True,
                )
                embedVar3.add_field(
                    name="Category", value=pop["results"][2]["category"], inline=True
                )
                embedVar3.add_field(
                    name="Comments",
                    value=pop["results"][2]["stats"]["comments"],
                    inline=True,
                )
                embedVar3.add_field(
                    name="Favorites",
                    value=pop["results"][2]["stats"]["favourites"],
                    inline=True,
                )
                embedVar3.add_field(
                    name="Deviation ID",
                    value=pop["results"][2]["deviationid"],
                    inline=True,
                )
                embedVar3.add_field(
                    name="URL", value=pop["results"][2]["url"], inline=True
                )
                embedVar3.set_image(url=pop["results"][2]["content"]["src"])
                embedVar3.set_thumbnail(
                    url=pop["results"][2]["author"]["usericon"])
                await ctx.send(embed=embedVar3)
                embedVar4 = discord.Embed(
                    title=pop["results"][3]["title"],
                    color=discord.Color.from_rgb(255, 250, 181),
                )
                embedVar4.add_field(
                    name="Creator",
                    value=pop["results"][3]["author"]["username"],
                    inline=True,
                )
                embedVar4.add_field(
                    name="Category", value=pop["results"][3]["category"], inline=True
                )
                embedVar4.add_field(
                    name="Comments",
                    value=pop["results"][3]["stats"]["comments"],
                    inline=True,
                )
                embedVar4.add_field(
                    name="Favorites",
                    value=pop["results"][3]["stats"]["favourites"],
                    inline=True,
                )
                embedVar4.add_field(
                    name="Deviation ID",
                    value=pop["results"][3]["deviationid"],
                    inline=True,
                )
                embedVar4.add_field(
                    name="URL", value=pop["results"][3]["url"], inline=True
                )
                embedVar4.set_image(url=pop["results"][3]["content"]["src"])
                embedVar4.set_thumbnail(
                    url=pop["results"][3]["author"]["usericon"])
                await ctx.send(embed=embedVar4)
                embedVar5 = discord.Embed(
                    title=pop["results"][4]["title"],
                    color=discord.Color.from_rgb(255, 250, 181),
                )
                embedVar5.add_field(
                    name="Creator",
                    value=pop["results"][4]["author"]["username"],
                    inline=True,
                )
                embedVar5.add_field(
                    name="Category", value=pop["results"][4]["category"], inline=True
                )
                embedVar5.add_field(
                    name="Comments",
                    value=pop["results"][4]["stats"]["comments"],
                    inline=True,
                )
                embedVar5.add_field(
                    name="Favorites",
                    value=pop["results"][4]["stats"]["favourites"],
                    inline=True,
                )
                embedVar5.add_field(
                    name="Deviation ID",
                    value=pop["results"][4]["deviationid"],
                    inline=True,
                )
                embedVar5.add_field(
                    name="URL", value=pop["results"][4]["url"], inline=True
                )
                embedVar5.set_image(url=pop["results"][4]["content"]["src"])
                embedVar5.set_thumbnail(
                    url=pop["results"][4]["author"]["usericon"])
                await ctx.send(embed=embedVar5)
            else:
                embedVar = discord.Embed(
                    color=discord.Color.from_rgb(255, 156, 192))
                embedVar.add_field(
                    name="Has More", value=pop["has_more"], inline=True)
                embedVar.add_field(
                    name="Estimated Total", value=pop["estimated_total"], inline=True
                )
                embedVar.add_field(name="Total", value=len(
                    pop["results"]), inline=True)
                embedVar.set_footer(
                    text="This only appears if the estimated total is less than 5 results. Info given here are for reference."
                )
                await ctx.send(embed=embedVar)
        except Exception as e:
            embedVar = discord.Embed(
                color=discord.Color.from_rgb(255, 214, 214))
            embedVar.description = "The query failed. Please try again"
            embedVar.add_field(name="Reason", value=e, inline=False)
            embedVar.add_field(name="Error", value=pop["error"], inline=True)
            embedVar.add_field(
                name="Error Description", value=pop["error_description"], inline=True
            )
            embedVar.add_field(name="Status", value=pop["status"], inline=True)
            await ctx.send(embed=embedVar)

    @deviantart_popular.error
    async def on_message_error(
        self, ctx: commands.Context, error: commands.CommandError
    ):
        if isinstance(error, commands.MissingRequiredArgument):
            embedVar = discord.Embed(color=discord.Color.from_rgb(255, 51, 51))
            embedVar.description = f"Missing a required argument: {error.param}"
            msg = await ctx.send(embed=embedVar, delete_after=10)
            await msg.delete(delay=10)


class DeviantArtV4(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="deviantart-tag-search", aliases=["da-tag-search"])
    async def tags(self, ctx, *, search: str):
        search = search.replace(" ", "%20")
        tags = get_tags(search)
        try:
            if int(len(tags["results"])) > 5:
                embedVar1 = discord.Embed(
                    title=tags["results"][0]["title"],
                    color=discord.Color.from_rgb(255, 99, 99),
                )
                embedVar1.add_field(
                    name="Creator",
                    value=tags["results"][0]["author"]["username"],
                    inline=True,
                )
                embedVar1.add_field(
                    name="Category", value=tags["results"][0]["category"], inline=True
                )
                embedVar1.add_field(
                    name="Comments",
                    value=tags["results"][0]["stats"]["comments"],
                    inline=True,
                )
                embedVar1.add_field(
                    name="Favorites",
                    value=tags["results"][0]["stats"]["favourites"],
                    inline=True,
                )
                embedVar1.add_field(
                    name="Deviation ID",
                    value=tags["results"][0]["deviationid"],
                    inline=True,
                )
                embedVar1.add_field(
                    name="URL", value=tags["results"][0]["url"], inline=True
                )
                embedVar1.set_image(url=tags["results"][0]["content"]["src"])
                embedVar1.set_thumbnail(
                    url=tags["results"][0]["author"]["usericon"])
                await ctx.send(embed=embedVar1)
                embedVar2 = discord.Embed(
                    title=tags["results"][1]["title"],
                    color=discord.Color.from_rgb(255, 242, 99),
                )
                embedVar2.add_field(
                    name="Creator",
                    value=tags["results"][1]["author"]["username"],
                    inline=True,
                )
                embedVar2.add_field(
                    name="Category", value=tags["results"][1]["category"], inline=True
                )
                embedVar2.add_field(
                    name="Comments",
                    value=tags["results"][1]["stats"]["comments"],
                    inline=True,
                )
                embedVar2.add_field(
                    name="Favorites",
                    value=tags["results"][1]["stats"]["favourites"],
                    inline=True,
                )
                embedVar2.add_field(
                    name="Deviation ID",
                    value=tags["results"][1]["deviationid"],
                    inline=True,
                )
                embedVar2.add_field(
                    name="URL", value=tags["results"][1]["url"], inline=True
                )
                embedVar2.set_image(url=tags["results"][1]["content"]["src"])
                embedVar2.set_thumbnail(
                    url=tags["results"][1]["author"]["usericon"])
                await ctx.send(embed=embedVar2)
                embedVar3 = discord.Embed(
                    title=tags["results"][2]["title"],
                    color=discord.Color.from_rgb(143, 255, 99),
                )
                embedVar3.add_field(
                    name="Creator",
                    value=tags["results"][2]["author"]["username"],
                    inline=True,
                )
                embedVar3.add_field(
                    name="Category", value=tags["results"][2]["category"], inline=True
                )
                embedVar3.add_field(
                    name="Comments",
                    value=tags["results"][2]["stats"]["comments"],
                    inline=True,
                )
                embedVar3.add_field(
                    name="Favorites",
                    value=tags["results"][2]["stats"]["favourites"],
                    inline=True,
                )
                embedVar3.add_field(
                    name="Deviation ID",
                    value=tags["results"][2]["deviationid"],
                    inline=True,
                )
                embedVar3.add_field(
                    name="URL", value=tags["results"][2]["url"], inline=True
                )
                embedVar3.set_image(url=tags["results"][2]["content"]["src"])
                embedVar3.set_thumbnail(
                    url=tags["results"][2]["author"]["usericon"])
                await ctx.send(embed=embedVar3)
                embedVar4 = discord.Embed(
                    title=tags["results"][3]["title"],
                    color=discord.Color.from_rgb(99, 255, 213),
                )
                embedVar4.add_field(
                    name="Creator",
                    value=tags["results"][3]["author"]["username"],
                    inline=True,
                )
                embedVar4.add_field(
                    name="Category", value=tags["results"][3]["category"], inline=True
                )
                embedVar4.add_field(
                    name="Comments",
                    value=tags["results"][3]["stats"]["comments"],
                    inline=True,
                )
                embedVar4.add_field(
                    name="Favorites",
                    value=tags["results"][3]["stats"]["favourites"],
                    inline=True,
                )
                embedVar4.add_field(
                    name="Deviation ID",
                    value=tags["results"][3]["deviationid"],
                    inline=True,
                )
                embedVar4.add_field(
                    name="URL", value=tags["results"][3]["url"], inline=True
                )
                embedVar4.set_image(url=tags["results"][3]["content"]["src"])
                embedVar4.set_thumbnail(
                    url=tags["results"][3]["author"]["usericon"])
                await ctx.send(embed=embedVar4)
                embedVar5 = discord.Embed(
                    title=tags["results"][4]["title"],
                    color=discord.Color.from_rgb(164, 99, 255),
                )
                embedVar5.add_field(
                    name="Creator",
                    value=tags["results"][4]["author"]["username"],
                    inline=True,
                )
                embedVar5.add_field(
                    name="Category", value=tags["results"][4]["category"], inline=True
                )
                embedVar5.add_field(
                    name="Comments",
                    value=tags["results"][4]["stats"]["comments"],
                    inline=True,
                )
                embedVar5.add_field(
                    name="Favorites",
                    value=tags["results"][4]["stats"]["favourites"],
                    inline=True,
                )
                embedVar5.add_field(
                    name="Deviation ID",
                    value=tags["results"][4]["deviationid"],
                    inline=True,
                )
                embedVar5.add_field(
                    name="URL", value=tags["results"][4]["url"], inline=True
                )
                embedVar5.set_image(url=tags["results"][4]["content"]["src"])
                embedVar5.set_thumbnail(
                    url=tags["results"][4]["author"]["usericon"])
                await ctx.send(embed=embedVar5)
            else:
                embedVar = discord.Embed(
                    color=discord.Color.from_rgb(255, 156, 192))
                embedVar.add_field(
                    name="Has More", value=tags["has_more"], inline=True)
                embedVar.add_field(
                    name="Total", value=len(tags["results"]), inline=True
                )
                embedVar.set_footer(
                    text="This only appears if the estimated total is less than 5 results. Info given here are for reference."
                )
                await ctx.send(embed=embedVar)
        except Exception as e:
            embedVar = discord.Embed(
                color=discord.Color.from_rgb(255, 214, 214))
            embedVar.description = "The query failed. Please try again"
            embedVar.add_field(name="Reason", value=e, inline=False)
            embedVar.add_field(name="Error", value=tags["error"], inline=True)
            embedVar.add_field(
                name="Error Description", value=tags["error_description"], inline=True
            )
            embedVar.add_field(
                name="Status", value=tags["status"], inline=True)
            await ctx.send(embed=embedVar)

    @tags.error
    async def on_message_error(
        self, ctx: commands.Context, error: commands.CommandError
    ):
        if isinstance(error, commands.MissingRequiredArgument):
            embedVar = discord.Embed(color=discord.Color.from_rgb(255, 51, 51))
            embedVar.description = f"Missing a required argument: {error.param}"
            msg = await ctx.send(embed=embedVar, delete_after=10)
            await msg.delete(delay=10)


class DeviantArtV5(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="deviantart-user", aliases=["da-user"])
    async def user(self, ctx, *, search: str):
        users = get_users(search)
        try:
            embedVar = discord.Embed(
                title=users["user"]["username"],
                color=discord.Color.from_rgb(255, 156, 192),
            )
            embedVar.add_field(
                name="Real Name", value=f"[{users['real_name']}]", inline=True
            )
            embedVar.add_field(
                name="Tagline", value=f"[{users['tagline']}]", inline=True
            )
            embedVar.add_field(
                name="Bio", value=f"[{users['bio']}]", inline=True)
            embedVar.add_field(
                name="Type", value=users["user"]["type"], inline=True)
            embedVar.add_field(
                name="User ID", value=users["user"]["userid"], inline=True
            )
            embedVar.add_field(
                name="Profile URL", value=users["profile_url"], inline=True
            )
            embedVar.add_field(
                name="Is Artist", value=users["user_is_artist"], inline=True
            )
            embedVar.add_field(
                name="Artist Level", value=users["artist_level"], inline=True
            )
            embedVar.add_field(
                name="Artist Specialty", value=users["artist_specialty"], inline=True
            )
            embedVar.add_field(
                name="Country", value=users["country"], inline=True)
            embedVar.add_field(
                name="Last Status", value=users["last_status"], inline=True
            )
            embedVar.add_field(
                name="User Deviations",
                value=users["stats"]["user_deviations"],
                inline=True,
            )
            embedVar.add_field(
                name="User Favorites",
                value=users["stats"]["user_favourites"],
                inline=True,
            )
            embedVar.add_field(
                name="User Comments", value=users["stats"]["user_comments"], inline=True
            )
            embedVar.add_field(
                name="Profile Views",
                value=users["stats"]["profile_pageviews"],
                inline=True,
            )
            embedVar.add_field(
                name="Profile Comments",
                value=users["stats"]["profile_comments"],
                inline=True,
            )
            embedVar.set_thumbnail(url=users["user"]["usericon"])
            await ctx.send(embed=embedVar)
        except Exception as e:
            embedVar = discord.Embed(
                color=discord.Color.from_rgb(255, 214, 214))
            embedVar.description = "The query failed. Please try again"
            embedVar.add_field(name="Reason", value=e, inline=False)
            await ctx.send(embed=embedVar)

    @user.error
    async def on_message_error(
        self, ctx: commands.Context, error: commands.CommandError
    ):
        if isinstance(error, commands.MissingRequiredArgument):
            embedVar = discord.Embed(color=discord.Color.from_rgb(255, 51, 51))
            embedVar.description = f"Missing a required argument: {error.param}"
            msg = await ctx.send(embed=embedVar, delete_after=10)
            await msg.delete(delay=10)


def setup(bot):
    bot.add_cog(DeviantArtV1(bot))
    bot.add_cog(DeviantArtV2(bot))
    bot.add_cog(DeviantArtV3(bot))
    bot.add_cog(DeviantArtV4(bot))
    bot.add_cog(DeviantArtV5(bot))
