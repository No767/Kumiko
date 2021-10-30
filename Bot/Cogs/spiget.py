import json

import ujson
import discord
import requests
from discord.ext import commands


def resource_search(search):
    link = f"https://api.spiget.org/v2/search/resources/{search}"
    headers = {"User-Agent": "Mozilla/5.0"}
    r = requests.get(link, headers=headers)
    data = r.text
    spiget = ujson.loads(data)
    return spiget


def resource_author(resource_creator):
    link = f"https://api.spiget.org/v2/resources/{resource_creator}/author"
    headers = {"User-Agent": "Mozilla/5.0"}
    r = requests.get(link, headers=headers)
    data = r.text
    spigetv2 = ujson.loads(data)
    return spigetv2


def plugin_version(resource_id):
    link = f"https://api.spiget.org/v2/resources/{resource_id}/versions/latest"
    headers = {"User-Agent": "Mozilla/5.0"}
    r = requests.get(link, headers=headers)
    data = r.text
    spigetv4 = ujson.loads(data)
    return spigetv4


def author_search(search):
    link = f"https://api.spiget.org/v2/search/authors/{search}"
    headers = {"User-Agent": "Mozilla/5.0"}
    r = requests.get(link, headers=headers)
    data = r.text
    spigetv5 = ujson.loads(data)
    return spigetv5


def author_details(author_id):
    link = f"https://api.spiget.org/v2/authors/{author_id}"
    headers = {"User-Agent": "Mozilla/5.0"}
    r = requests.get(link, headers=headers)
    data = r.text
    spigetv6 = ujson.loads(data)
    return spigetv6

def stats():
    link = "https://api.spiget.org/v2/status"
    headers = {"User-Agent": "Mozilla/5.0"}
    r = requests.get(link, headers=headers)
    data = r.text
    spigetv7 = ujson.loads(data)
    return spigetv7

class SpigetV2(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="spiget-search")
    async def on_message(self, ctx, *, search: str):
        resource = resource_search(search)
        author_id = resource[0]["author"]["id"]
        author_details_v1 = author_details(author_id)
        resource_id = resource[0]["id"]
        thumbnail = "https://www.spigotmc.org/" + resource[0]["icon"]["url"]
        file_size = str(resource[0]["file"]["size"]) + str(
            resource[0]["file"]["sizeUnit"]
        )
        download_url_external_false = "https://spigotmc.org/" + str(
            resource[0]["file"]["url"]
        )

        link = f"https://api.spiget.org/v2/resources/{resource_id}/versions"
        headers = {"User-Agent": "Mozilla/5.0"}
        r = requests.get(link, headers=headers)
        data = r.text
        spigetv3 = ujson.loads(data)

        try:
            if resource[0]["file"]["type"] in "external":
                embedVar = discord.Embed(color=discord.Color.from_rgb(173, 156, 255))
                embedVar.add_field(
                    name="Plugin Info",
                    value=f"Name >> {resource[0]['name']}\nTag >> {resource[0]['tag']}\nAuthor >> {author_details_v1['name']}\nDownloads >> {resource[0]['downloads']}\nRating >> {resource[0]['rating']['average']}",
                    inline=False,
                )
                embedVar.add_field(
                    name="Tested Versions",
                    value=str(resource[0]["testedVersions"])
                    .replace("[", "")
                    .replace("]", "")
                    .replace("'", ""),
                    inline=False,
                )
                embedVar.add_field(
                    name="Latest Plugin Version",
                    value=str(plugin_version(resource_id)["name"]),
                    inline=False,
                )
                embedVar.add_field(
                    name="Plugin Versions",
                    value=str([name["name"] for name in spigetv3])
                    .replace("[", "")
                    .replace("]", "")
                    .replace("'", ""),
                    inline=False,
                )
                embedVar.add_field(
                    name="Download Info",
                    value=f"Type >> {resource[0]['file']['type']}",
                    inline=False,
                )
                embedVar.add_field(
                    name="Download URL",
                    value=f"{resource[0]['file']['externalUrl']}",
                    inline=False,
                )
                embedVar.set_thumbnail(url=str(thumbnail))
                await ctx.send(embed=embedVar)
            else:
                embedVar = discord.Embed(color=discord.Color.from_rgb(173, 156, 255))
                embedVar.add_field(
                    name="Plugin Info",
                    value=f"Name >> {resource[0]['name']}\nTag >> {resource[0]['tag']}\nAuthor >> {author_details_v1['name']}\nDownloads >> {resource[0]['downloads']}\nRating >> {resource[0]['rating']['average']}",
                    inline=False,
                )
                embedVar.add_field(
                    name="Tested Versions",
                    value=str(resource[0]["testedVersions"])
                    .replace("[", "")
                    .replace("]", "")
                    .replace("'", ""),
                    inline=False,
                )
                embedVar.add_field(
                    name="Latest Plugin Version",
                    value=str(plugin_version(resource_id)["name"]),
                    inline=False,
                )
                embedVar.add_field(
                    name="Plugin Versions",
                    value=str([name["name"] for name in spigetv3])
                    .replace("[", "")
                    .replace("]", "")
                    .replace("'", ""),
                    inline=False,
                )
                embedVar.add_field(
                    name="Download Info",
                    value=f"Type >> {resource[0]['file']['type']}\nSize >> {file_size}",
                    inline=False,
                )
                embedVar.add_field(
                    name="Download URL",
                    value=f"{download_url_external_false}",
                    inline=False,
                )
                embedVar.set_thumbnail(url=str(thumbnail))
                await ctx.send(embed=embedVar)
        except Exception as e:
            embedVar = discord.Embed(color=discord.Color.from_rgb(173, 156, 255))
            embedVar.description = f"The query failed. Please Try Again.\nReason: {e}"
            await ctx.send(embed=embedVar)


class Spigetv3(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="spiget-author")
    async def on_message(self, ctx, *, search: str):
        author = author_search(search)
        author_id = author[0]["id"]
        author_thumbnail = author[0]["icon"]["url"]
        linkv2 = f"https://api.spiget.org/v2/authors/{author_id}/resources"
        headers = {"User-Agent": "Mozilla/5.0"}
        author_request = requests.get(linkv2, headers=headers)
        datav2 = author_request.text
        spigetv4 = ujson.loads(datav2)
        try:
            embedVar = discord.Embed(color=discord.Color.from_rgb(173, 156, 255))
            embedVar.add_field(
                name="Author Name", value=f"{author[0]['name']}", inline=False
            )
            embedVar.add_field(
                name="Author Resources",
                value=str([name["name"] for name in spigetv4])
                .replace("[", "")
                .replace("]", "")
                .replace("'", ""),
                inline=False,
            )
            embedVar.set_thumbnail(url=str(author_thumbnail))
            await ctx.send(embed=embedVar)
        except Exception as e:
            embedVar = discord.Embed(color=discord.Color.from_rgb(173, 156, 255))
            embedVar.description = f"The query failed. Please Try Again.\nReason: {e}"
            await ctx.send(embed=embedVar)

class SpigetV4(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name="spiget-stats")
    async def on_message(self, ctx):
        try:
            total_stats = stats()
            embedVar = discord.Embed(color=discord.Color.from_rgb(173, 156, 255))
            embedVar.add_field(name="Resources", value=total_stats['stats']["resources"], inline=True)
            embedVar.add_field(name="Authors", value=total_stats['stats']["authors"], inline=True)
            embedVar.add_field(name="Categories", value=total_stats['stats']["categories"], inline=True)
            embedVar.add_field(name="Resource Updates", value=total_stats['stats']["resource_updates"], inline=True)
            embedVar.add_field(name="Resource Versions", value=total_stats['stats']["resource_versions"], inline=True)
            embedVar.add_field(name="Reviews", value=total_stats['stats']["reviews"], inline=True)
            await ctx.send(embed=embedVar)
        except Exception as e:
            embedVar = discord.Embed(color=discord.Color.from_rgb(173, 156, 255))
            embedVar.description = f"The query failed. Please Try Again.\nReason: {e}"
            await ctx.send(embed=embedVar)
            
class SpigetV5(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name="spiget-status")
    async def on_message(self, ctx):
        try:
            link = "https://api.spiget.org/v2/"
            headers = {"User-Agent": "Mozilla/5.0"}
            r = requests.get(link, headers=headers)
            embedVar = discord.Embed(color=discord.Color.from_rgb(173, 156, 255))
            embedVar.add_field(name="Status", value=r.status_code, inline=True)
            await ctx.send(embed=embedVar)
        except Exception as e:
            embedVar = discord.Embed(color=discord.Color.from_rgb(173, 156, 255))
            embedVar.description = f"The query failed. Please Try Again.\nReason: {e}"
            await ctx.send(embed=embedVar)

def setup(bot):
    bot.add_cog(SpigetV2(bot))
    bot.add_cog(Spigetv3(bot))
    bot.add_cog(SpigetV4(bot))
    bot.add_cog(SpigetV5(bot))
