import discord
import os
from discord.ext import commands
from instagram_private_api import Client, ClientCompatPatch
from dotenv import load_dotenv

load_dotenv()

user_name = os.getenv("InstagramUserName")
password = os.getenv("InstagramPassword")

api = Client(user_name, password)
api.generate_uuid()

# Requires Client ID
class instagram(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    @commands.command(name="iginfo")
    async def on_message(self, ctx, search:str):
        username_feed = api.user_info(search)
        embedVar = discord.Embed()
        embedVar.description = f"{api.user_info(search)}"
        await ctx.send(embed=embedVar)


class iguserfeed(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="iguserfeed")
    async def on_message(self, ctx, search:str):
        user_feed = api.user_feed(search)
        await ctx.send(api.user_feed(search))


class iginfo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="igusersearch")
    async def on_message(self, ctx, search: str):
        top_search = api.search_users(search)
        search_users_formatted = """
        Instagram Username >> {users}
        """.format(**api.search_users(search))
        embedVar = discord.Embed()
        embedVar.description = f"{search_users_formatted}"
        await ctx.send(embed=embedVar)


class top_search(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="igtaginfo")
    async def on_message(self, ctx, search: str):
        best_search = api.tag_info(search)
        tag_info_formatted = """
        Tag ID >> {id}
        Name >> {name}
        Follow Status >> {follow_status}
        Following >> {following}
        Tag Media Count >> {formatted_media_count}
        Description >> {description}
        API Status >> {status}
        
        **Related Tags**
        {related_tags}
        """.format(**api.tag_info(search))
        embedVar = discord.Embed()
        embedVar.description = f"{tag_info_formatted}"
        await ctx.send(embed=embedVar)

class username_checker(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name="igusernamecheck")
    async def on_message(self, ctx, search:str):
        username_check = api.check_username(search)
        username_check_formatter = """
        Username >> {username}
        Available >> {available}
        Existing User Password >> {existing_user_password}
        Error >> {error}
        Error Type >> {error_type}
        API Status >> {status}
        """.format(**api.check_username(search))
        embedVar = discord.Embed()
        embedVar.description = f"{username_check_formatter}"
        await ctx.send(embed=embedVar)

class suggested_users(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name="igsuggestedusers")
    async def on_message(self, ctx, search:str):
        user_suggested_formatted = api.discover_chaining(search)    
        await ctx.send(user_suggested_formatted)

def setup(bot):
    bot.add_cog(instagram(bot))
    bot.add_cog(iguserfeed(bot))
    bot.add_cog(iginfo(bot))
    bot.add_cog(top_search(bot))
    bot.add_cog(username_checker(bot))
    bot.add_cog(suggested_users(bot))
