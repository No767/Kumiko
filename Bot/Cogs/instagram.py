import discord
import os
from discord.ext import commands
from instagram_private_api import Client
from instagram_private_api import ClientCompatPatch
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

    @commands.command(name="iguserinfo")
    async def on_message(self, ctx, search: str):
        username_feed = api.user_info(search)
        username_info_format = f"""
        **Basic Information**
        
        Instagram Username >> {api.user_info(search)['user']['username']}
        Full Name >> {api.user_info(search)['user']['full_name']}
        Is Private >> {api.user_info(search)['user']['is_private']}
        Profile Pic ID >> {api.user_info(search)['user']['profile_pic_id']}
        Is Verified >> {api.user_info(search)['user']['is_verified']}
        
        **User Information**
        
        Media / Post Count >> {api.user_info(search)['user']['media_count']}
        Total IGTV Videos >> {api.user_info(search)['user']['total_igtv_videos']}
        Usertag Count >> {api.user_info(search)['user']['usertags_count']}
        Follower Count >> {api.user_info(search)['user']['follower_count']}
        Following Count >> {api.user_info(search)['user']['following_count']}
        Biography >> 
        {api.user_info(search)['user']['biography']}
        External URL >> {api.user_info(search)['user']['external_url']}
        External Lynx URL >>> {api.user_info(search)['user']['external_lynx_url']}
        
        **API Contact Status**
        API Status >> {api.user_info(search)['status']}
        """
        embedVar = discord.Embed(title="Instagram User Info")
        embedVar.description = f"{username_info_format}"
        embedurl = api.user_info(search)["user"]["profile_pic_url"]
        embedVar.set_thumbnail(url=embedurl)
        await ctx.send(embed=embedVar)


class iginfo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="igusersearch")
    async def on_message(self, ctx, search: str):
        top_search = api.search_users(search)
        search_users_formatted = f"""
        **Results**
        
        Results >> {api.search_users(search)['num_results']}
        
        **User Information**
        
        PK >> {api.search_users(search)['users'][0]['pk']}
        Username >> {api.search_users(search)['users'][0]['username']}
        Full Name >> {api.search_users(search)['users'][0]['full_name']}
        Is Private >> {api.search_users(search)['users'][0]['is_private']}
        Is Verified >> {api.search_users(search)['users'][0]['is_verified']}
        Account Badges >> {api.search_users(search)['users'][0]['account_badges']}
        
        **API Contact Status**
        
        API >> {api.search_users(search)['status']}
        """
        embedVar = discord.Embed(title="Instagram User Search")
        embedVar.description = f"{search_users_formatted}"
        embedpfp = api.search_users(search)["users"][0]["profile_pic_url"]
        embedVar.set_thumbnail(url=embedpfp)
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
        
        **Related Tags**
        {related_tags}
        
        **API Contact Status**
        
        API Status >> {status}
        """.format(
            **api.tag_info(search)
        )
        embedVar = discord.Embed(title="Instagram Tag Search")
        embedVar.description = f"{tag_info_formatted}"
        await ctx.send(embed=embedVar)


class username_checker(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="igusernamecheck")
    async def on_message(self, ctx, search: str):
        username_check = api.check_username(search)
        username_check_formatter = """
        Username >> {username}
        Available >> {available}
        Existing User Password >> {existing_user_password}
        Error >> {error}
        Error Type >> {error_type}
        
        **API Contact Status**
        
        API Status >> {status}
        """.format(
            **api.check_username(search)
        )
        embedVar = discord.Embed(title="Instagram Username Checker")
        embedVar.description = f"{username_check_formatter}"
        await ctx.send(embed=embedVar)


def setup(bot):
    bot.add_cog(instagram(bot))
    bot.add_cog(iginfo(bot))
    bot.add_cog(top_search(bot))
    bot.add_cog(username_checker(bot))
