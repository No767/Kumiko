import os

import discord
from discord.ext import commands
from dotenv import load_dotenv
from discord.ext.commands import cooldown, BucketType
from instagram_private_api import Client, ClientCompatPatch

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
    @commands.cooldown(5, 15)
    async def on_message(self, ctx, search: str):
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
    @commands.cooldown(5, 15)
    async def on_message(self, ctx, search: str):
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
    @commands.cooldown(5, 15)
    async def on_message(self, ctx, search: str):
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
    @commands.cooldown(5, 15)
    async def on_message(self, ctx, search: str):
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


class userfeed(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="iguserfeed")
    @commands.cooldown(5, 15)
    async def on_message(self, ctx, search: str):
        userfeed_formatter = f"""
        {api.user_feed(search)["items"][0]['caption']['text']}
        """
        userfeedurl = api.user_feed(search)["items"][0]["carousel_media"][0][
            "image_versions2"
        ]["candidates"][0]["url"]
        userfeedpfpurl = api.user_feed(
            search)["items"][0]["user"]["profile_pic_url"]
        userfeed_likecount = api.user_feed(search)["items"][0]["like_count"]
        embedVar = discord.Embed()
        embedVar.description = f"{userfeed_formatter}"
        embedVar.set_image(url=userfeedurl)
        embedVar.set_thumbnail(url=userfeedpfpurl)
        embedVar.set_footer(text=f"Likes >> {userfeed_likecount}")
        await ctx.send(embed=embedVar)


def setup(bot):
    bot.add_cog(instagram(bot))
    bot.add_cog(iginfo(bot))
    bot.add_cog(top_search(bot))
    bot.add_cog(username_checker(bot))
    bot.add_cog(userfeed(bot))
