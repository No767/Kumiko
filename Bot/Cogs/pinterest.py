import os

import aiohttp
import discord
import orjson
from discord.ext import commands
from dotenv import load_dotenv
import asyncio
import uvloop

load_dotenv()

Pinterest_API_Access_Token = os.getenv("Pinterest_Access_Token")


class PinterestV1(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="pinterest-user", aliases=["pt-user"])
    async def user(self, ctx):
        async with aiohttp.ClientSession(json_serialize=orjson.dumps) as session:
            headers = {"Authorization": f"Bearer {Pinterest_API_Access_Token}"}
            async with session.get(
                "https://api.pinterest.com/v5/user_account", headers=headers
            ) as r:
                user = await r.text()
                try:
                    embedVar = discord.Embed(
                        title=user["username"],
                        color=discord.Color.from_rgb(255, 222, 179),
                    )
                    embedVar.add_field(
                        name="Account Type", value=user["account_type"], inline=True
                    )
                    embedVar.add_field(
                        name="Website URL",
                        value=f"[{user['website_url']}]",
                        inline=True,
                    )
                    embedVar.set_thumbnail(url=user["profile_image"])
                    await ctx.send(embed=embedVar)
                except Exception as e:
                    embedVar = discord.Embed(
                        color=discord.Color.from_rgb(255, 51, 51))
                    embedVar.description = "It seems like this query failed."
                    embedVar.add_field(name="Reason", value=e, inline=True)
                    embedVar.add_field(
                        name="Code", value=user["code"], inline=True)
                    embedVar.add_field(
                        name="Message", value=user["message"], inline=True
                    )
                    await ctx.send(embed=embedVar)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


class PinterestV2(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="pinterest-pin", aliases=["pt-pin"])
    async def user(self, ctx, id: int):
        headers = {"Authorization": f"Bearer {Pinterest_API_Access_Token}"}
        async with aiohttp.ClientSession(json_serialize=orjson.dumps) as session:
            async with session.get(f"https://api.pinterest.com/v5/pins/{id}", headers=headers) as r:
                pin = await r.json()
                try:
                    embedVar = discord.Embed(
                        title=pin["title"], color=discord.Color.from_rgb(255, 187, 179)
                    )
                    embedVar.add_field(
                        name="Description", value=pin["description"], inline=True
                    )
                    embedVar.add_field(
                        name="Alt Text", value=pin["alt_text"], inline=True)
                    embedVar.add_field(
                        name="Board Owner", value=pin["board_owner"]["username"], inline=True
                    )
                    embedVar.add_field(
                        name="Board ID", value=pin["board_id"], inline=True)
                    embedVar.add_field(name="ID", value=pin["id"], inline=True)
                    embedVar.add_field(name="Link", value=pin["link"], inline=True)
                    embedVar.add_field(
                        name="Created At",
                        value=str(pin["created_at"]).replace("T", " "),
                        inline=True,
                    )
                    embedVar.set_image(url=pin["media"]["originals"]["url"])
                    await ctx.send(embed=embedVar)
                except Exception as e:
                    embedVar = discord.Embed(color=discord.Color.from_rgb(255, 51, 51))
                    embedVar.description = "It seems like this query failed."
                    embedVar.add_field(name="Reason", value=e, inline=True)
                    embedVar.add_field(name="Code", value=pin["code"], inline=True)
                    embedVar.add_field(
                        name="Message", value=pin["message"], inline=True)
                    await ctx.send(embed=embedVar)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    @user.error
    async def on_message_error(
        self, ctx: commands.Context, error: commands.CommandError
    ):
        if isinstance(error, commands.MissingRequiredArgument):
            embedVar = discord.Embed(color=discord.Color.from_rgb(255, 51, 51))
            embedVar.description = f"Missing a required argument: {error.param}"
            msg = await ctx.send(embed=embedVar, delete_after=10)
            await msg.delete(delay=10)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


class PinterestV3(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="pinterest-board", aliases=["pt-board"])
    async def board(self, ctx, board_id: int):
        board = get_board(board_id)
        board_list = get_list_board(board_id)
        headers = {"Authorization": f"Bearer {Pinterest_API_Access_Token}"}
        async with aiohttp.ClientSession(json_serialize=orjson.dumps) as session:
            async with session.get(f"https://api.pinterest.com/v5/boards/{board_id}", headers=headers) as r:
                board = await r.json()
                async with session.get(f"https://api.pinterest.com/v5/boards/{board_id}/pins", headers=headers) as response:
                    board_list = await response.json()
                    try:
                        embedVar = discord.Embed(
                            color=discord.Color.from_rgb(192, 255, 173))
                        embedVar.add_field(name="Name", value=board["name"], inline=True)
                        embedVar.add_field(
                            name="Description", value=board["description"], inline=True
                        )
                        embedVar.add_field(
                            name="Owner", value=board["owner"]["username"], inline=True
                        )
                        embedVar.add_field(name="ID", value=board["id"], inline=True)
                        embedVar.add_field(
                            name="Privacy", value=board["privacy"], inline=True)
                        embedVar.add_field(
                            name="Total Pins", value=len(board_list["items"]), inline=True
                        )
                    except Exception as e:
                        embedVar = discord.Embed(color=discord.Color.from_rgb(255, 51, 51))
                        embedVar.description = "It seems like this query failed."
                        embedVar.add_field(name="Reason", value=e, inline=True)
                        embedVar.add_field(name="Code", value=board["code"], inline=True)
                        embedVar.add_field(
                            name="Message", value=board["message"], inline=True)
                        await ctx.send(embed=embedVar)
                        
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    @board.error
    async def on_message_error(
        self, ctx: commands.Context, error: commands.CommandError
    ):
        if isinstance(error, commands.MissingRequiredArgument):
            embedVar = discord.Embed(color=discord.Color.from_rgb(255, 51, 51))
            embedVar.description = f"Missing a required argument: {error.param}"
            msg = await ctx.send(embed=embedVar, delete_after=10)
            await msg.delete(delay=10)
            
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


def setup(bot):
    bot.add_cog(PinterestV1(bot))
    bot.add_cog(PinterestV2(bot))
    bot.add_cog(PinterestV3(bot))
