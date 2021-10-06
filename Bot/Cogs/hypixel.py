import json
import os
import re

import discord
import requests
from discord import Embed
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

hypixel_api_key = os.getenv("Hypixel_API_Key")


def hypixel_lookup(username):
    link = f"https://api.hypixel.net/player?name={username}&key={hypixel_api_key}"
    r = requests.get(link)
    player_data = r.text
    hypixel_player = json.loads(player_data)
    return hypixel_player


def player_status(uuid):
    link = f"https://api.hypixel.net/status?uuid={uuid}&key={hypixel_api_key}"
    r = requests.get(link)
    player_data = r.text
    player_statusv2 = json.loads(player_data)
    return player_statusv2


def player_count():
    link = f"https://api.hypixel.net/counts?key={hypixel_api_key}"
    r = requests.get(link)
    player_data = r.text
    player_countv2 = json.loads(player_data)
    return player_countv2


class hypixel_api(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="hypixel")
    async def on_message(self, ctx, *, search: str):
        search = search.replace(" ", "%20")
        player = hypixel_lookup(search)
        if str(player["success"]) == "True":
            discord_embed = discord.Embed()
            discord_embed.description = f"""
                ** Info on {player['player']['displayname']} **
                

                """
            await ctx.send(embed=discord_embed)
        else:
            embedVar = discord.Embed()
            embedVar.description = f"""
                The query was not successful. 
                
                Debug:
                
                Success >> {player['success']}
                Cause >> {player['cause']}
                """
            await ctx.send(embed=embedVar)

class hypixel_player_count(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="hypixelcount")
    async def on_message(self, ctx):
        status = player_count()
        if str(status["success"]) == "True":
            embedVar = discord.Embed()
            embedVar.description = f"""
                **Games Player Count**

                Main Lobby >> {status['games']['MAIN_LOBBY']['players']}

                Tournament Lobby >> {status['games']['TOURNAMENT_LOBBY']['players']}

                SMP >> {status['games']['SMP']['players']}

                Housing >> {status['games']['HOUSING']['players']}

                Pit >> {status['games']['PIT']['players']}

                TNTGames >> {status['games']['TNTGAMES']['players']}

                Replay >> {status['games']['REPLAY']['players']}

                Bedwars >> {status['games']['BEDWARS']['players']}

                Survival Games >> {status['games']['SURVIVAL_GAMES']['players']}

                Skyblock >> {status['games']['SKYBLOCK']['players']}

                Murder Mystery >> {status['games']['MURDER_MYSTERY']['players']}

                Skywars >> {status['games']['SKYWARS']['players']}

                UHC >> {status['games']['UHC']['players']}

                Arcade >> {status['games']['ARCADE']['players']}

                Build Battle >> {status['games']['BUILD_BATTLE']['players']}

                Duels >> {status['games']['DUELS']['players']}
                """

            await ctx.send(embed=embedVar)

class hypixel_status(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="hypixelplayerstatus")
    async def on_message(self, ctx, *, uuid: str):
        player_statusv3 = player_status(uuid)
        if str(player_statusv3["success"]) == "True":
            embedVar = discord.Embed()
            embedVar.description = f"""
            Success >> {player_statusv3['success']}
            UUID >> {player_statusv3['uuid']}
            Online >> {player_statusv3['session']['online']}
            """
            await ctx.send(embed=embedVar)
        else:
            embedVar = discord.Embed()
            embedVar.description = f"""
            The query was not successful. 

            Debug:

            Success >> {player_statusv3['success']}
            Cause >> {player_statusv3['cause']}
            """
            await ctx.send(embed=embedVar)


def setup(bot):
    bot.add_cog(hypixel_api(bot))
    bot.add_cog(hypixel_status(bot))
    bot.add_cog(hypixel_player_count(bot))
