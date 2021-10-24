import json
import os
import re

import discord
import requests
from discord import Embed
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()


def resource_search(search):
    link = f"https://api.spiget.org/v2/search/resources/{search}"
    headers = {"User-Agent": "Mozilla/5.0"}
    r = requests.get(link, headers=headers)
    data = r.text
    return json.loads(data)


def resource_author(search):
    link = f"https://api.spiget.org/v2/search/resources/{search}/author"
    headers = {"User-Agent": "Mozilla/5.0"}
    r = requests.get(link, headers=headers)
    data = r.text
    spigetv2 = json.loads(data)
    return spigetv2


def plugin_version(resource_id):
    link = f"https://api.spiget.org/v2/resources/{resource_id}/versions/latest"
    headers = {"User-Agent": "Mozilla/5.0"}
    r = requests.get(link, headers=headers)
    data = r.text
    spigetv4 = json.loads(data)
    return spigetv4


class SpigetV2(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="spiget-search")
    async def on_message(self, ctx, *, search: str):
        resource = resource_search(search)
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
        spigetv3 = json.loads(data)
        try:
            if resource[0]["file"]["type"] in "external":
                embedVar = discord.Embed()
                embedVar.add_field(
                    name="Plugin Info",
                    value=f"Name >> {resource[0]['name']}\nTag >> {resource[0]['tag']}\nAuthor >> {resource[0]['name']}\nDownloads >> {resource[0]['downloads']}\nRating >> {resource[0]['rating']['average']}",
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
                    value=f"{resource[0]['file']['externalUrl']}",
                    inline=False,
                )
                embedVar.set_thumbnail(url=str(thumbnail))
                await ctx.send(embed=embedVar)
            else:
                embedVar = discord.Embed()
                embedVar.add_field(
                    name="Plugin Info",
                    value=f"Name >> {resource[0]['name']}\nTag >> {resource[0]['tag']}\nAuthor >> {resource[0]['name']}\nDownloads >> {resource[0]['downloads']}\nRating >> {resource[0]['rating']['average']}",
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
            await ctx.send(e)


def setup(bot):
    bot.add_cog(SpigetV2(bot))
