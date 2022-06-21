import asyncio
import os

import aiohttp
import discord
import orjson
import simdjson
import uvloop
from discord.commands import Option, SlashCommandGroup
from discord.ext import commands, pages
from dotenv import load_dotenv
from exceptions import NoItemsError

load_dotenv()

Bearer_Token = os.getenv("Twitter_Bearer_Token")
parser = simdjson.Parser()


class TwitterV1(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    twitter = SlashCommandGroup("twitter", "Commands for the Twitter service")

    @twitter.command(name="search")
    async def twitter_search(
        self, ctx, *, user: Option(str, "The username to search up")
    ):
        """Returns up to 25 recent tweets from the given the Twitter user"""
        async with aiohttp.ClientSession(json_serialize=orjson.dumps) as session:
            headers = {"Authorization": f"Bearer {Bearer_Token}"}
            params = {
                "query": f"from:{user}",
                "expansions": "author_id,attachments.media_keys",
                "tweet.fields": "created_at",
                "user.fields": "name,profile_image_url,username",
                "media.fields": "preview_image_url",
            }
            async with session.get(
                "https://api.twitter.com/2/tweets/search/recent",
                headers=headers,
                params=params,
            ) as r:
                data = await r.content.read()
                dataMain = parser.parse(data, recursive=True)
                try:
                    if len(dataMain["data"]) == 0:
                        raise NoItemsError
                    else:
                        discord.Embed()
                        excludedKeys = {
                            "entities",
                            "retweeted_status",
                            "quoted_status",
                            "metadata",
                            "id",
                            "id_str",
                            "source",
                            "in_reply_to_status_id",
                            "in_reply_to_status_id_str",
                            "in_reply_to_user_id",
                            "in_reply_to_user_id_str",
                            "text",
                            "source",
                            "is_quote_status",
                            "quoted_status_id",
                            "quoted_status_id_str",
                            "possibly_sensitive",
                            "contributors",
                            "in_reply_to_screen_name",
                            "truncated",
                            "extended_entities",
                            "user",
                            "favorited",
                            "retweeted",
                            "lang",
                        }
                        mainPages = pages.Paginator(
                            pages=[
                                discord.Embed(
                                    title=f'{[dictItem3["username"] for dictItem3 in dataMain["includes"]["users"]]} - {[dictItem2["name"] for dictItem2 in dataMain["includes"]["users"]]}',
                                    description=[mainItem["text"]],
                                ).set_thumbnail(
                                    url=str(
                                        [
                                            str(dictItem2["profile_image_url"]).replace(
                                                "_normal", "_bigger"
                                            )
                                            for dictItem2 in dataMain["includes"][
                                                "users"
                                            ]
                                        ]
                                    )
                                    .replace("'", "")
                                    .replace("[", "")
                                    .replace("]", "")
                                )
                                for mainItem in dataMain["data"]
                            ]
                        )
                        await mainPages.respond(ctx.interaction, ephemeral=False)
                        # for dictItem in dataMain["statuses"]:
                        #     if "extended_entities" in dictItem:
                        #         for keys, val in dictItem.items():
                        #             if keys not in excludedKeys:
                        #                 embed.add_field(
                        #                     name=str(keys)
                        #                     .replace("_", " ")
                        #                     .capitalize(),
                        #                     value=val,
                        #                     inline=True,
                        #                 )
                        #                 embed.remove_field(-6)
                        #         for v in dictItem["extended_entities"].items():
                        #             embed.set_image(url=v[1][0]["media_url_https"])
                        #         embed.description = dictItem["text"]
                        #         embed.set_thumbnail(
                        #             url=str(
                        #                 dictItem["user"]["profile_image_url_https"]
                        #             ).replace("_normal", "_bigger")
                        #         )
                        #         await ctx.respond(embed=embed)
                        #     else:
                        #         for keys2, val2 in dictItem.items():
                        #             if keys2 not in excludedKeys:
                        #                 embed.add_field(
                        #                     name=str(keys2)
                        #                     .replace("_", " ")
                        #                     .capitalize(),
                        #                     value=val2,
                        #                     inline=True,
                        #                 )
                        #                 embed.remove_field(-6)
                        #         embed.description = dictItem["text"]
                        #         embed.set_thumbnail(
                        #             url=str(
                        #                 dictItem["user"]["profile_image_url_https"]
                        #             ).replace("_normal", "_bigger")
                        #         )
                        #         await ctx.respond(embed=embed)
                except NoItemsError:
                    embedError = discord.Embed()
                    embedError.description = f"It looks like there were no tweets from the user {user} found within the past 5 days... Please try again"
                    await ctx.respond(embed=embedError)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    @twitter.command(name="user")
    async def twitter_user(self, ctx, *, user: str):
        """Returns Info about the given Twitter user"""
        async with aiohttp.ClientSession(json_serialize=orjson.dumps) as session:
            headers = {"Authorization": f"Bearer {Bearer_Token}"}
            params = {"q": user, "count": 1}
            async with session.get(
                "https://api.twitter.com/1.1/users/search.json",
                headers=headers,
                params=params,
            ) as resp:
                data2 = await resp.content.read()
                dataMain2 = parser.parse(data2, recursive=True)
                itemFilter = {
                    "profile_image_url_https",
                    "id",
                    "id_str",
                    "name",
                    "description",
                    "entities",
                    "status",
                    "profile_background_color",
                    "profile_background_image_url",
                    "profile_background_image_url_https",
                    "profile_background_tile",
                    "profile_image_url",
                    "profile_link_color",
                    "profile_sidebar_border_color",
                    "profile_sidebar_fill_color",
                    "profile_text_color",
                    "profile_use_background_image",
                    "has_extended_profile",
                    "default_profile",
                    "default_profile_image",
                    "follow_request_sent",
                    "following",
                    "notifications",
                    "translator_type",
                    "url",
                    "profile_banner_url",
                    "withheld_in_countries",
                }
                embedVar = discord.Embed()
                try:
                    if len(dataMain2) == 0:
                        raise ValueError
                    else:
                        for userItem in dataMain2:
                            if "profile_banner_url" in userItem:
                                for keys, val in userItem.items():
                                    if keys not in itemFilter:
                                        embedVar.add_field(
                                            name=str(keys)
                                            .replace("_", " ")
                                            .capitalize(),
                                            value=f"[{val}]",
                                            inline=True,
                                        )
                                embedVar.title = userItem["name"]
                                embedVar.description = userItem["description"]
                                embedVar.set_image(
                                    url=str(userItem["profile_banner_url"])
                                )
                                embedVar.set_thumbnail(
                                    url=str(
                                        userItem["profile_image_url_https"]
                                    ).replace("_normal", "_bigger")
                                )
                                await ctx.respond(embed=embedVar)
                            else:
                                for keys2, val2 in userItem.items():
                                    if keys2 not in itemFilter:
                                        embedVar.add_field(
                                            name=str(keys2)
                                            .replace("_", " ")
                                            .capitalize(),
                                            value=f"[{val2}]",
                                            inline=True,
                                        )
                                embedVar.title = userItem["name"]
                                embedVar.description = userItem["description"]
                                embedVar.set_thumbnail(
                                    url=str(
                                        userItem["profile_image_url_https"]
                                    ).replace("_normal", "_bigger")
                                )
                                await ctx.respond(embed=embedVar)

                except ValueError:
                    embedErrorMain = discord.Embed()
                    embedErrorMain.description = "Sorry, but the user that you searched for doesn't exist. Please try again"
                    await ctx.respond(embed=embedErrorMain)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


def setup(bot):
    bot.add_cog(TwitterV1(bot))
