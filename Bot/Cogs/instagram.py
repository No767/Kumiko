import asyncio
import os

import discord
import uvloop
from discord.ext import commands
from dotenv import load_dotenv
from instagram_private_api import Client

load_dotenv()

user_name = os.getenv("InstagramUserNameV2")
password = os.getenv("InstagramPasswordV2")

api = Client(user_name, password)
api.generate_uuid()


# Requires Client ID
class instagram(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="iguserinfo")
    @commands.cooldown(rate=1, per=20)
    async def info(self, ctx, search: str):
        try:
            embedVar = discord.Embed(
                title="Instagram User Info", color=discord.Color.from_rgb(255, 214, 214)
            )
            embedVar.add_field(
                name="Instragram Username",
                value=f"{api.user_info(search)['user']['username']}",
                inline=True,
            )
            embedVar.add_field(
                name="Full Name",
                value=f"{api.user_info(search)['user']['full_name']}",
                inline=True,
            )
            embedVar.add_field(
                name="Is Private",
                value=f"{api.user_info(search)['user']['is_private']}",
                inline=True,
            )
            embedVar.add_field(
                name="Profile Pic ID",
                value=f"{api.user_info(search)['user']['profile_pic_id']}",
                inline=True,
            )
            embedVar.add_field(
                name="Is Verified",
                value=f"{api.user_info(search)['user']['is_verified']}",
                inline=True,
            )
            embedVar.add_field(
                name="Media / Post Count",
                value=f"{api.user_info(search)['user']['media_count']}",
                inline=True,
            )
            embedVar.add_field(
                name="Total IGTV Videos",
                value=f"{api.user_info(search)['user']['total_igtv_videos']}",
                inline=True,
            )
            embedVar.add_field(
                name="Usertag Count",
                value=f"{api.user_info(search)['user']['usertags_count']}",
                inline=True,
            )
            embedVar.add_field(
                name="Follower Count",
                value=f"{api.user_info(search)['user']['follower_count']}",
                inline=True,
            )
            embedVar.add_field(
                name="Following Count",
                value=f"{api.user_info(search)['user']['following_count']}",
                inline=True,
            )
            embedVar.add_field(
                name="Biography",
                value=f"{api.user_info(search)['user']['biography']}",
                inline=True,
            )
            embedVar.add_field(
                name="API Status",
                value=f"{api.user_info(search)['status']}",
                inline=True,
            )
            embedVar.set_thumbnail(url=api.user_info(search)[
                                   "user"]["profile_pic_url"])
            await ctx.send(embed=embedVar)
        except Exception as e:
            embedVar = discord.Embed(color=discord.Color.from_rgb(255, 51, 51))
            embedVar.description = (
                f"The query has failed. Please try again.\nReason:{e}"
            )
            await ctx.send(embed=embedVar)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    @info.error
    async def on_message_error(
        self, ctx: commands.Context, error: commands.CommandError
    ):
        if isinstance(error, commands.CommandOnCooldown):
            embedVar = discord.Embed(color=discord.Color.from_rgb(255, 51, 51))
            embedVar.description = f"Currently on cooldown. Please try again after {round(error.retry_after, 1)} seconds"
            msg = await ctx.send(embed=embedVar, delete_after=10)
            await msg.delete(delay=10)
        elif isinstance(error, commands.MissingRequiredArgument):
            embedVar = discord.Embed(color=discord.Color.from_rgb(255, 51, 51))
            embedVar.description = f"Missing a requireed argument: {error.param}"
            msg = await ctx.send(embed=embedVar, delete_after=10)
            await msg.delete(delay=10)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


class iginfo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="igusersearch")
    @commands.cooldown(rate=1, per=20)
    async def user_search(self, ctx, search: str):
        try:
            embedVar = discord.Embed(
                title="Instagram User Search",
                color=discord.Color.from_rgb(255, 237, 214),
            )
            embedVar.add_field(
                name="Amount of Results",
                value=f"{api.search_users(search)['num_results']}",
                inline=True,
            )
            embedVar.add_field(
                name="PK",
                value=f"{api.search_users(search)['users'][0]['pk']}",
                inline=True,
            )
            embedVar.add_field(
                name="Username",
                value=f"{api.search_users(search)['users'][0]['username']}",
                inline=True,
            )
            embedVar.add_field(
                name="Full Name",
                value=f"{api.search_users(search)['users'][0]['full_name']}",
                inline=True,
            )
            embedVar.add_field(
                name="Is Private",
                value=f"{api.search_users(search)['users'][0]['is_private']}",
                inline=True,
            )
            embedVar.add_field(
                name="Is Verified",
                value=f"{api.search_users(search)['users'][0]['is_verified']}",
                inline=True,
            )
            embedVar.add_field(
                name="Account Badges",
                value=f"{api.search_users(search)['users'][0]['account_badges']}",
                inline=True,
            )
            embedVar.add_field(
                name="API Status",
                value=f"{api.search_users(search)['status']}",
                inline=True,
            )
            embedVar.set_thumbnail(
                url=api.search_users(search)["users"][0]["profile_pic_url"]
            )
            await ctx.send(embed=embedVar)
        except Exception as e:
            embedVar = discord.Embed(color=discord.Color.from_rgb(255, 51, 51))
            embedVar.description = (
                f"The query has failed. Please try again.\nReason:{e}"
            )
            await ctx.send(embed=embedVar)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    @user_search.error
    async def on_message_error(
        self, ctx: commands.Context, error: commands.CommandError
    ):
        if isinstance(error, commands.CommandOnCooldown):
            embedVar = discord.Embed(color=discord.Color.from_rgb(255, 51, 51))
            embedVar.description = f"Currently on cooldown. Please try again after {round(error.retry_after, 1)} seconds"
            msg = await ctx.send(embed=embedVar, delete_after=10)
            await msg.delete(delay=10)
        elif isinstance(error, commands.MissingRequiredArgument):
            embedVar = discord.Embed(color=discord.Color.from_rgb(255, 51, 51))
            embedVar.description = f"Missing a requireed argument: {error.param}"
            msg = await ctx.send(embed=embedVar, delete_after=10)
            await msg.delete(delay=10)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


class top_search(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="igtaginfo")
    @commands.cooldown(rate=1, per=20)
    async def tag(self, ctx, search: str):
        try:
            embedVar = discord.Embed(
                title="Instagram Tag Search",
                color=discord.Color.from_rgb(239, 255, 214),
            )
            embedVar.add_field(
                name="Tag ID", value=f"{api.tag_info(search)['id']}", inline=True
            )
            embedVar.add_field(
                name="Name", value=f"{api.tag_info(search)['name']}", inline=True
            )
            embedVar.add_field(
                name="Follow Status",
                value=f"{api.tag_info(search)['follow_status']}",
                inline=True,
            )
            embedVar.add_field(
                name="Following",
                value=f"{api.tag_info(search)['following']}",
                inline=True,
            )
            embedVar.add_field(
                name="Tag Media Count",
                value=f"{api.tag_info(search)['media_count']}",
                inline=True,
            )
            embedVar.add_field(
                name="Description",
                value=f"{api.tag_info(search)['description']}",
                inline=True,
            )
            embedVar.add_field(
                name="Related Tags",
                value=f"{api.tag_info(search)['related_tags']}",
                inline=True,
            )
            embedVar.add_field(
                name="API Status",
                value=f"{api.tag_info(search)['status']}",
                inline=True,
            )
            await ctx.send(embed=embedVar)
        except Exception as e:
            embedVar = discord.Embed(color=discord.Color.from_rgb(255, 51, 51))
            embedVar.description = (
                f"The query has failed. Please try again.\nReason:{e}"
            )
            await ctx.send(embed=embedVar)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    @tag.error
    async def on_message_error(
        self, ctx: commands.Context, error: commands.CommandError
    ):
        if isinstance(error, commands.CommandOnCooldown):
            embedVar = discord.Embed(color=discord.Color.from_rgb(255, 51, 51))
            embedVar.description = f"Currently on cooldown. Please try again after {round(error.retry_after, 1)} seconds"
            msg = await ctx.send(embed=embedVar, delete_after=10)
            await msg.delete(delay=10)
        elif isinstance(error, commands.MissingRequiredArgument):
            embedVar = discord.Embed(color=discord.Color.from_rgb(255, 51, 51))
            embedVar.description = f"Missing a requireed argument: {error.param}"
            msg = await ctx.send(embed=embedVar, delete_after=10)
            await msg.delete(delay=10)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


class username_checker(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="igusernamecheck")
    @commands.cooldown(rate=1, per=20)
    async def username(self, ctx, search: str):
        try:
            embedVar = discord.Embed(
                title="Instagram Username Checker",
                color=discord.Color.from_rgb(214, 255, 229),
            )
            embedVar.add_field(
                name="Username",
                value=f"{api.check_username(search)['username']}",
                inline=True,
            )
            embedVar.add_field(
                name="Available",
                value=f"{api.check_username(search)['available']}",
                inline=True,
            )
            embedVar.add_field(
                name="Existing User Password",
                value=f"{api.check_username(search)['existing_user_password']}",
                inline=True,
            )
            embedVar.add_field(
                name="Error",
                value=f"{api.check_username(search)['error']}",
                inline=True,
            )
            embedVar.add_field(
                name="Error Type",
                value=f"{api.check_username(search)['error_type']}",
                inline=True,
            )
            embedVar.add_field(
                name="API Status",
                value=f"{api.check_username(search)['status']}",
                inline=True,
            )
            await ctx.send(embed=embedVar)
        except Exception as e:
            embedVar = discord.Embed(color=discord.Color.from_rgb(255, 51, 51))
            embedVar.description = (
                f"The query has failed. Please try again.\nReason:{e}"
            )
            await ctx.send(embed=embedVar)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    @username.error
    async def on_message_error(
        self, ctx: commands.Context, error: commands.CommandError
    ):
        if isinstance(error, commands.CommandOnCooldown):
            embedVar = discord.Embed(color=discord.Color.from_rgb(255, 51, 51))
            embedVar.description = f"Currently on cooldown. Please try again after {round(error.retry_after, 1)} seconds"
            msg = await ctx.send(embed=embedVar, delete_after=10)
            await msg.delete(delay=10)
        elif isinstance(error, commands.MissingRequiredArgument):
            embedVar = discord.Embed(color=discord.Color.from_rgb(255, 51, 51))
            embedVar.description = f"Missing a requireed argument: {error.param}"
            msg = await ctx.send(embed=embedVar, delete_after=10)
            await msg.delete(delay=10)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


class userfeed(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="iguserfeed")
    @commands.cooldown(rate=1, per=20)
    async def feed(self, ctx, search: str):
        try:
            embedVar = discord.Embed()
            embedVar.description = api.user_feed(
                search)["items"][0]["caption"]["text"]
            embedVar.set_image(
                url=api.user_feed(search)["items"][0]["image_versions2"]["candidates"][
                    0
                ]["url"]
            )
            embedVar.set_thumbnail(
                url=api.user_feed(search)[
                    "items"][0]["user"]["profile_pic_url"]
            )
            embedVar.set_footer(
                text=f"Likes >> {api.user_feed(search)['items'][0]['like_count']}"
            )
            await ctx.send(embed=embedVar)
        except Exception as e:
            embedVar = discord.Embed(color=discord.Color.from_rgb(255, 51, 51))
            embedVar.description = (
                f"The query has failed. Please try again.\nReason:{e}"
            )
            await ctx.send(embed=embedVar)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    @feed.error
    async def on_message_error(
        self, ctx: commands.Context, error: commands.CommandError
    ):
        if isinstance(error, commands.CommandOnCooldown):
            embedVar = discord.Embed(color=discord.Color.from_rgb(255, 51, 51))
            embedVar.description = f"Currently on cooldown. Please try again after {round(error.retry_after, 1)} seconds"
            msg = await ctx.send(embed=embedVar, delete_after=10)
            await msg.delete(delay=10)
        elif isinstance(error, commands.MissingRequiredArgument):
            embedVar = discord.Embed(color=discord.Color.from_rgb(255, 51, 51))
            embedVar.description = f"Missing a requireed argument: {error.param}"
            msg = await ctx.send(embed=embedVar, delete_after=10)
            await msg.delete(delay=10)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


def setup(bot):
    bot.add_cog(instagram(bot))
    bot.add_cog(iginfo(bot))
    bot.add_cog(top_search(bot))
    bot.add_cog(username_checker(bot))
    bot.add_cog(userfeed(bot))
