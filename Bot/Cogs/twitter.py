import os
import aiohttp
import orjson
import discord
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
            params = {"q": "from:{user}", "count": 1}
            async with session.get("https://api.twitter.com/1.1/search/tweets.json", headers=headers, params=params) as r:
                data = await r.json()
                if data["statuses"] is None:
                    embedVar = discord.Embed()
                    embedVar.description = "Sadly there are no tweets from this user."
                    embedVar.add_field(name="Result Count", value=data["meta"]["result_count"], inline=True)
                    await ctx.send(embed=embedVar)
                else:
                    embedVar = discord.Embed()
                    embedVar.add_field(name="Tweet Created At", value=data["statuses"]["created_at"], inline=True)
                    embedVar.add_field(name="Name", value=data["statuses"][0]["user"]["name"], inline=True)
                    embedVar.add_field(name="Username", value=data["statuses"][0]["user"]["screen_name"], inline=True)
                    embedVar.add_field(name="Text", value=data["statuses"]["text"], inline=False)
                    embedVar.add_field(name="URLs", value=data["statuses"]["urls"][1]["expanded_url"], inline=True)
                    embedVar.add_field(name="Original Tweet URL", value=data["statuses"][0]["extended_entities"]["media"][0]["url"], inline=True)
                    embedVar.set_thumbnail(url=data["statuses"][0]["user"]["profile_image_url"])
                    embedVar.set_image(url=data["statuses"][0]["extended_entities"]["media"][0]["media_url_https"])
                    await ctx.send(embed=embedVar)

def setup(bot):
    bot.add_cog(TwitterV1(bot))
                    
                    