from discord.ext import commands
from dotenv import load_dotenv
import requests
import ujson
import os
import discord

load_dotenv()

Pinterest_API_Access_Token = os.getenv("Pinterest_Access_Token")

def get_self_user():
    link = "https://api.pinterest.com/v5/user_account"
    headers = {"Authorization": f"Bearer {Pinterest_API_Access_Token}"}
    r = requests.get(link, headers=headers)
    return ujson.loads(r.text)

def get_pin(id):
    link = f"https://api.pinterest.com/v5/pins/{id}"
    headers = {"Authorization": f"Bearer {Pinterest_API_Access_Token}"}
    r = requests.get(link, headers=headers)
    return ujson.loads(r.text)

def get_board(board_id):
    link = f"https://api.pinterest.com/v5/boards/{board_id}"
    headers = {"Authorization": f"Bearer {Pinterest_API_Access_Token}"}
    r = requests.get(link, headers=headers)
    return ujson.loads(r.text)

def get_list_board(board_id):
    link = f"https://api.pinterest.com/v5/boards/{board_id}/pins"
    headers = {"Authorization": f"Bearer {Pinterest_API_Access_Token}"}
    r = requests.get(link, headers=headers)
    return ujson.loads(r.text)
class PinterestV1(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="pinterest-user", aliases=["pt-user"])
    async def user(self, ctx):
        user = get_self_user()
        try:
            embedVar = discord.Embed(title=user['username'], color=discord.Color.from_rgb(255, 222, 179))
            embedVar.add_field(name="Account Type", value=user['account_type'], inline=True)
            embedVar.add_field(name="Website URL", value=f"[{user['website_url']}]", inline=True)
            embedVar.set_thumbnail(url=user['profile_image'])
            await ctx.send(embed=embedVar) 
        except Exception as e:
            embedVar = discord.Embed(color=discord.Color.from_rgb(255, 51, 51))
            embedVar.description = "It seems like this query failed."
            embedVar.add_field(name="Reason", value=e, inline=True)
            embedVar.add_field(name="Code", value=user['code'], inline=True)
            embedVar.add_field(name="Message", value=user['message'], inline=True)
            await ctx.send(embed=embedVar)

class PinterestV2(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="pinterest-pin", aliases=["pt-pin"])
    async def user(self, ctx, id:int):
        pin = get_pin(id)
        try:
            embedVar = discord.Embed(title=pin['title'], color=discord.Color.from_rgb(255, 187, 179))
            embedVar.add_field(name="Description", value=pin['description'], inline=True)
            embedVar.add_field(name="Alt Text", value=pin['alt_text'], inline=True)
            embedVar.add_field(name="Board Owner", value=pin['board_owner']['username'], inline=True)
            embedVar.add_field(name="Board ID", value=pin['board_id'], inline=True)
            embedVar.add_field(name="ID", value=pin['id'], inline=True)
            embedVar.add_field(name="Link", value=pin['link'], inline=True)
            embedVar.add_field(name="Created At", value=str(pin['created_at']).replace("T", " "), inline=True)
            embedVar.set_image(url=pin['media']['originals']['url'])
            await ctx.send(embed=embedVar)
        except Exception as e:
            embedVar = discord.Embed(color=discord.Color.from_rgb(255, 51, 51))
            embedVar.description = "It seems like this query failed."
            embedVar.add_field(name="Reason", value=e, inline=True)
            embedVar.add_field(name="Code", value=pin['code'], inline=True)
            embedVar.add_field(name="Message", value=pin['message'], inline=True)
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
            
class PinterestV3(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command(name="pinterest-board", aliases=["pt-board"])
    async def board(self, ctx, board_id:int):
        board = get_board(board_id)
        board_list = get_list_board(board_id)
        try:
            embedVar = discord.Embed(color=discord.Color.from_rgb(192, 255, 173))
            embedVar.add_field(name="Name", value=board['name'], inline=True)
            embedVar.add_field(name="Description", value=board['description'], inline=True)
            embedVar.add_field(name="Owner", value=board['owner']['username'], inline=True)
            embedVar.add_field(name="ID", value=board['id'], inline=True)
            embedVar.add_field(name="Privacy", value=board['privacy'], inline=True)
            embedVar.add_field(name="Total Pins", value=len(board_list['items']), inline=True)
        except Exception as e:
            embedVar = discord.Embed(color=discord.Color.from_rgb(255, 51, 51))
            embedVar.description = "It seems like this query failed."
            embedVar.add_field(name="Reason", value=e, inline=True)
            embedVar.add_field(name="Code", value=board['code'], inline=True)
            embedVar.add_field(name="Message", value=board['message'], inline=True)
            await ctx.send(embed=embedVar)
            
    @board.error
    async def on_message_error(
        self, ctx: commands.Context, error: commands.CommandError
    ):
        if isinstance(error, commands.MissingRequiredArgument):
            embedVar = discord.Embed(color=discord.Color.from_rgb(255, 51, 51))
            embedVar.description = f"Missing a required argument: {error.param}"
            msg = await ctx.send(embed=embedVar, delete_after=10)
            await msg.delete(delay=10)
def setup(bot):
    bot.add_cog(PinterestV1(bot))
    bot.add_cog(PinterestV2(bot))
    bot.add_cog(PinterestV3(bot))
