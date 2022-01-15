import asyncio
import os

import aiohttp
import discord
import orjson
import uvloop
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

Bearer_Token = os.getenv("Twitter_Bearer_Token")


class TwitterV1(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="twitter-search", aliases=["ts"])
    async def twitter_search(self, ctx, *, user: str):
        async with aiohttp.ClientSession(json_serialize=orjson.dumps) as session:
            headers = {"Authorization": f"Bearer {Bearer_Token}"}
            params = {"q": f"from:{user}", "count": 5}
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
                                url=str(
                                    data["statuses"][0]["user"]["profile_image_url"]
                                ).replace("_normal", "_bigger")
                            )
                            embedVar.set_image(
                                url=data["statuses"][0]["extended_entities"]["media"][
                                    0
                                ]["media_url_https"]
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
                                url=str(
                                    data["statuses"][0]["user"]["profile_image_url"]
                                ).replace("_normal", "_bigger")
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
                                url=str(
                                    data["statuses"][1]["user"]["profile_image_url"]
                                ).replace("_normal", "_bigger")
                            )
                            embedVar2.set_image(
                                url=data["statuses"][1]["extended_entities"]["media"][
                                    0
                                ]["media_url_https"]
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
                                url=str(
                                    data["statuses"][1]["user"]["profile_image_url"]
                                ).replace("_normal", "_bigger")
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
                                url=str(
                                    data["statuses"][2]["user"]["profile_image_url"]
                                ).replace("_normal", "_bigger")
                            )
                            embedVar3.set_image(
                                url=data["statuses"][2]["extended_entities"]["media"][
                                    0
                                ]["media_url_https"]
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
                                url=str(
                                    data["statuses"][2]["user"]["profile_image_url"]
                                ).replace("_normal", "_bigger")
                            )
                            await ctx.send(embed=embedVar3)
                        if "extended_entities" in data["statuses"][3]:
                            embedVar4 = discord.Embed()
                            embedVar4.add_field(
                                name="Tweet Created At",
                                value=data["statuses"][3]["created_at"],
                                inline=True,
                            )
                            embedVar4.add_field(
                                name="Name",
                                value=data["statuses"][3]["user"]["name"],
                                inline=True,
                            )
                            embedVar4.add_field(
                                name="Username",
                                value=data["statuses"][3]["user"]["screen_name"],
                                inline=True,
                            )
                            embedVar4.add_field(
                                name="Text",
                                value=data["statuses"][3]["text"],
                                inline=True,
                            )
                            embedVar4.set_thumbnail(
                                url=str(
                                    data["statuses"][3]["user"]["profile_image_url"]
                                ).replace("_normal", "_bigger")
                            )
                            embedVar4.set_image(
                                url=data["statuses"][3]["extended_entities"]["media"][
                                    0
                                ]["media_url_https"]
                            )
                            await ctx.send(embed=embedVar4)
                        else:
                            embedVar4 = discord.Embed()
                            embedVar4.add_field(
                                name="Tweet Created At",
                                value=data["statuses"][3]["created_at"],
                                inline=True,
                            )
                            embedVar4.add_field(
                                name="Name",
                                value=data["statuses"][3]["user"]["name"],
                                inline=True,
                            )
                            embedVar4.add_field(
                                name="Username",
                                value=data["statuses"][3]["user"]["screen_name"],
                                inline=True,
                            )
                            embedVar4.add_field(
                                name="Text",
                                value=data["statuses"][3]["text"],
                                inline=True,
                            )
                            embedVar4.set_thumbnail(
                                url=str(
                                    data["statuses"][3]["user"]["profile_image_url"]
                                ).replace("_normal", "_bigger")
                            )
                            await ctx.send(embed=embedVar4)
                        if "extended_entities" in data["statuses"][4]:
                            embedVar5 = discord.Embed()
                            embedVar5.add_field(
                                name="Tweet Created At",
                                value=data["statuses"][4]["created_at"],
                                inline=True,
                            )
                            embedVar5.add_field(
                                name="Name",
                                value=data["statuses"][4]["user"]["name"],
                                inline=True,
                            )
                            embedVar5.add_field(
                                name="Username",
                                value=data["statuses"][4]["user"]["screen_name"],
                                inline=True,
                            )
                            embedVar5.add_field(
                                name="Text",
                                value=data["statuses"][4]["text"],
                                inline=True,
                            )
                            embedVar5.set_thumbnail(
                                url=str(
                                    data["statuses"][4]["user"]["profile_image_url"]
                                ).replace("_normal", "_bigger")
                            )
                            embedVar5.set_image(
                                url=data["statuses"][4]["extended_entities"]["media"][
                                    0
                                ]["media_url_https"]
                            )
                            await ctx.send(embed=embedVar5)
                        else:
                            embedVar5 = discord.Embed()
                            embedVar5.add_field(
                                name="Tweet Created At",
                                value=data["statuses"][4]["created_at"],
                                inline=True,
                            )
                            embedVar5.add_field(
                                name="Name",
                                value=data["statuses"][4]["user"]["name"],
                                inline=True,
                            )
                            embedVar5.add_field(
                                name="Username",
                                value=data["statuses"][4]["user"]["screen_name"],
                                inline=True,
                            )
                            embedVar5.add_field(
                                name="Text",
                                value=data["statuses"][4]["text"],
                                inline=True,
                            )
                            embedVar5.set_thumbnail(
                                url=str(
                                    data["statuses"][4]["user"]["profile_image_url"]
                                ).replace("_normal", "_bigger")
                            )
                            await ctx.send(embed=embedVar5)
                except Exception as e:
                    embedError = discord.Embed()
                    embedError.description = "Something went wrong. Please try again."
                    embedError.add_field(name="Error", value=e, inline=True)
                    await ctx.send(embed=embedError)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    @twitter_search.error
    async def on_message_error(
        self, ctx: commands.Context, error: commands.CommandError
    ):
        if isinstance(error, commands.MissingRequiredArgument):
            embedVar = discord.Embed(color=discord.Color.from_rgb(255, 51, 51))
            embedVar.description = f"Missing a requireed argument: {error.param}"
            msg = await ctx.send(embed=embedVar, delete_after=10)
            await msg.delete(delay=10)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


class TwitterV2(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="twitter-user", aliases=["tu"])
    async def twitter_user(self, ctx, *, user: str):
        async with aiohttp.ClientSession(json_serialize=orjson.dumps) as session:
            headers = {"Authorization": f"Bearer {Bearer_Token}"}
            params = {"q": user, "count": 1}
            async with session.get(
                "https://api.twitter.com/1.1/users/search.json",
                headers=headers,
                params=params,
            ) as resp:
                data2 = await resp.json()
                try:
                    if "profile_banner_url" in data2[0]:
                        embedVar = discord.Embed()
                        embedVar.title = f"{data2[0]['name']}'s Twitter Profile"
                        embedVar.add_field(
                            name="Username", value=data2[0]["screen_name"], inline=True
                        )
                        embedVar.add_field(
                            name="Location",
                            value=f'[{data2[0]["location"]}]',
                            inline=True,
                        )
                        embedVar.add_field(
                            name="Description",
                            value=f'[{data2[0]["description"]}]',
                            inline=True,
                        )
                        embedVar.add_field(
                            name="Followers",
                            value=data2[0]["followers_count"],
                            inline=True,
                        )
                        embedVar.add_field(
                            name="Friends Count",
                            value=data2[0]["friends_count"],
                            inline=True,
                        )
                        embedVar.add_field(
                            name="Listed Count",
                            value=data2[0]["listed_count"],
                            inline=True,
                        )
                        embedVar.add_field(
                            name="Amount of Tweets/Statuses",
                            value=data2[0]["statuses_count"],
                            inline=True,
                        )
                        embedVar.add_field(
                            name="Created At",
                            value=str(data2[0]["created_at"]
                                      ).replace("+0000", ""),
                            inline=True,
                        )
                        embedVar.add_field(
                            name="Verified", value=data2[0]["verified"], inline=True
                        )
                        embedVar.set_thumbnail(
                            url=str(data2[0]["profile_image_url_https"]).replace(
                                "_normal", ""
                            )
                        )
                        embedVar.set_image(url=data2[0]["profile_banner_url"])
                        await ctx.send(embed=embedVar)
                    else:
                        embedVar = discord.Embed()
                        embedVar.title = f"{data2[0]['name']}'s Twitter Profile"
                        embedVar.add_field(
                            name="Username", value=data2[0]["screen_name"], inline=True
                        )
                        embedVar.add_field(
                            name="Location",
                            value=f'[{data2[0]["location"]}]',
                            inline=True,
                        )
                        embedVar.add_field(
                            name="Description",
                            value=f'[{data2[0]["description"]}]',
                            inline=True,
                        )
                        embedVar.add_field(
                            name="Followers",
                            value=data2[0]["followers_count"],
                            inline=True,
                        )
                        embedVar.add_field(
                            name="Friends Count",
                            value=data2[0]["friends_count"],
                            inline=True,
                        )
                        embedVar.add_field(
                            name="Listed Count",
                            value=data2[0]["listed_count"],
                            inline=True,
                        )
                        embedVar.add_field(
                            name="Amount of Tweets/Statuses",
                            value=data2[0]["statuses_count"],
                            inline=True,
                        )
                        embedVar.add_field(
                            name="Created At",
                            value=str(data2[0]["created_at"]
                                      ).replace("+0000", ""),
                            inline=True,
                        )
                        embedVar.add_field(
                            name="Verified", value=data2[0]["verified"], inline=True
                        )
                        embedVar.set_thumbnail(
                            url=str(data2[0]["profile_image_url_https"]).replace(
                                "_normal", ""
                            )
                        )
                        await ctx.send(embed=embedVar)

                except Exception as e:
                    embedError2 = discord.Embed()
                    embedError2.description = "Something went wrong. Please try again."
                    embedError2.add_field(name="Error", value=e, inline=True)
                    await ctx.send(embed=embedError2)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    @twitter_user.error
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
    bot.add_cog(TwitterV1(bot))
    bot.add_cog(TwitterV2(bot))
