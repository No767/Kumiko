import os

import aiohttp
import discord
import orjson
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

Bearer_Token = os.getenv("Twitter_Bearer_Token")

# Note that currently the Twitter service is using v1.1, which is going to get replaced by the v2 later. Once v2 introduces the data for videos and links to the media, im gonna rewrite it to use the v2 version instead


class TwitterV1(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="twitter-search", aliases=["ts"])
    async def twitter_search(self, ctx, *, user: str):
        async with aiohttp.ClientSession(json_serialize=orjson.dumps) as session:
            headers = {"Authorization": f"Bearer {Bearer_Token}"}
            params = {"q": f"from:{user}", "count": 3}
            async with session.get(
                "https://api.twitter.com/1.1/search/tweets.json",
                headers=headers,
                params=params,
            ) as r:
                data = await r.json()
                try:
                    if data["statuses"] is None:
                        embedVar = discord.Embed()
                        embedVar.description = (
                            "Sadly there are no tweets from this user."
                        )
                        embedVar.add_field(
                            name="Result Count",
                            value=data["meta"]["result_count"],
                            inline=True,
                        )
                        await ctx.send(embed=embedVar)
                    else:
                        if "extended_entities" in data["statuses"][0]:
                            embedVar = discord.Embed()
                            embedVar.add_field(
                                name="Tweet Created At",
                                value=data["statuses"][0]["created_at"],
                                inline=True,
                            )
                            embedVar.add_field(
                                name="Name",
                                value=data["statuses"][0]["user"]["name"],
                                inline=True,
                            )
                            embedVar.add_field(
                                name="Username",
                                value=data["statuses"][0]["user"]["screen_name"],
                                inline=True,
                            )
                            embedVar.add_field(
                                name="Text",
                                value=data["statuses"][0]["text"],
                                inline=True,
                            )
                            embedVar.set_thumbnail(
                                url=data["statuses"][0]["user"]["profile_image_url"]
                            )
                            embedVar.set_image(
                                data["statuses"][0]["extended_entities"]["media"][0][
                                    "media_url_https"
                                ]
                            )
                            await ctx.send(embed=embedVar)
                        else:
                            embedVar = discord.Embed()
                            embedVar.add_field(
                                name="Tweet Created At",
                                value=data["statuses"][0]["created_at"],
                                inline=True,
                            )
                            embedVar.add_field(
                                name="Name",
                                value=data["statuses"][0]["user"]["name"],
                                inline=True,
                            )
                            embedVar.add_field(
                                name="Username",
                                value=data["statuses"][0]["user"]["screen_name"],
                                inline=True,
                            )
                            embedVar.add_field(
                                name="Text",
                                value=data["statuses"][0]["text"],
                                inline=True,
                            )
                            embedVar.set_thumbnail(
                                url=data["statuses"][0]["user"]["profile_image_url"]
                            )
                            await ctx.send(embed=embedVar)

                            if "extended_entities" in data["statuses"][1]:
                                embedVar2 = discord.Embed()
                                embedVar2.add_field(
                                    name="Tweet Created At",
                                    value=data["statuses"][1]["created_at"],
                                    inline=True,
                                )
                                embedVar2.add_field(
                                    name="Name",
                                    value=data["statuses"][1]["user"]["name"],
                                    inline=True,
                                )
                                embedVar2.add_field(
                                    name="Username",
                                    value=data["statuses"][1]["user"]["screen_name"],
                                    inline=True,
                                )
                                embedVar2.add_field(
                                    name="Text",
                                    value=data["statuses"][1]["text"],
                                    inline=True,
                                )
                                embedVar2.set_thumbnail(
                                    url=data["statuses"][1]["user"]["profile_image_url"]
                                )
                                embedVar2.set_image(
                                    url=data["statuses"][1]["extended_entities"][
                                        "media"
                                    ][0]["media_url_https"]
                                )
                                await ctx.send(embed=embedVar2)
                            else:
                                embedVar2 = discord.Embed()
                                embedVar2.add_field(
                                    name="Tweet Created At",
                                    value=data["statuses"][1]["created_at"],
                                    inline=True,
                                )
                                embedVar2.add_field(
                                    name="Name",
                                    value=data["statuses"][1]["user"]["name"],
                                    inline=True,
                                )
                                embedVar2.add_field(
                                    name="Username",
                                    value=data["statuses"][1]["user"]["screen_name"],
                                    inline=True,
                                )
                                embedVar2.add_field(
                                    name="Text",
                                    value=data["statuses"][1]["text"],
                                    inline=True,
                                )
                                embedVar2.set_thumbnail(
                                    url=data["statuses"][1]["user"]["profile_image_url"]
                                )
                                await ctx.send(embed=embedVar2)

                            if "extended_entities" in data["statuses"][2]:
                                embedVar3 = discord.Embed()
                                embedVar3.add_field(
                                    name="Tweet Created At",
                                    value=data["statuses"][2]["created_at"],
                                    inline=True,
                                )
                                embedVar3.add_field(
                                    name="Name",
                                    value=data["statuses"][2]["user"]["name"],
                                    inline=True,
                                )
                                embedVar3.add_field(
                                    name="Username",
                                    value=data["statuses"][2]["user"]["screen_name"],
                                    inline=True,
                                )
                                embedVar3.add_field(
                                    name="Text",
                                    value=data["statuses"][2]["text"],
                                    inline=True,
                                )
                                embedVar3.set_thumbnail(
                                    url=data["statuses"][2]["user"]["profile_image_url"]
                                )
                                embedVar3.set_image(
                                    url=data["statuses"][2]["extended_entities"][
                                        "media"
                                    ][0]["media_url_https"]
                                )
                                await ctx.send(embed=embedVar3)
                            else:
                                embedVar3 = discord.Embed()
                                embedVar3.add_field(
                                    name="Tweet Created At",
                                    value=data["statuses"][2]["created_at"],
                                    inline=True,
                                )
                                embedVar3.add_field(
                                    name="Name",
                                    value=data["statuses"][2]["user"]["name"],
                                    inline=True,
                                )
                                embedVar3.add_field(
                                    name="Username",
                                    value=data["statuses"][2]["user"]["screen_name"],
                                    inline=True,
                                )
                                embedVar3.add_field(
                                    name="Text",
                                    value=data["statuses"][2]["text"],
                                    inline=True,
                                )
                                embedVar3.set_thumbnail(
                                    url=data["statuses"][2]["user"]["profile_image_url"]
                                )
                                await ctx.send(embed=embedVar3)
                except Exception as e:
                    embedError = discord.Embed()
                    embedError.description = "Something went wrong. Please try again."
                    embedError.add_field(name="Error", value=e, inline=True)
                    await ctx.send(embed=embedError)

    @twitter_search.error
    async def on_message_error(
        self, ctx: commands.Context, error: commands.CommandError
    ):
        if isinstance(error, commands.MissingRequiredArgument):
            embedVar = discord.Embed(color=discord.Color.from_rgb(255, 51, 51))
            embedVar.description = f"Missing a requireed argument: {error.param}"
            msg = await ctx.send(embed=embedVar, delete_after=10)
            await msg.delete(delay=10)


def setup(bot):
    bot.add_cog(TwitterV1(bot))
