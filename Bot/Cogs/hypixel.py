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


def hypixel_lookup(uuid):
    link = f"https://api.hypixel.net/player?uuid={uuid}&key={hypixel_api_key}"
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


def player_ranked_skywars(uuid):
    link = f"https://api.hypixel.net/player/ranked/skywars?uuid={uuid}&key={hypixel_api_key}"
    r = requests.get(link)
    ranked_skywars = r.text
    skywars = json.loads(ranked_skywars)
    return skywars


def http_status():
    link = f"https://api.hypixel.net/status?key={hypixel_api_key}"
    r = requests.get(link)
    return r.status_code


class hypixel_api(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="hypixel")
    async def on_message(self, ctx, *, uuid: str):
        player = hypixel_lookup(uuid)
        online = player_status(uuid)
        skywars = player_ranked_skywars(uuid)
        if str(player["success"]) == "True":
            discord_embed = discord.Embed(title=f"Player Info")
            discord_embed.description = f"""
                Username >> {player['player']['displayname']}
                ID >> {player['player']['_id']}
                UUID >> {player['player']['uuid']}
                Known Aliases >> {str(player['player']['knownAliases']).replace("[", " ").replace("]", " ").replace("'", " ")}  
                Online Status >> {online['session']['online']}
                
                **Success or Not?**
                Success >> {player['success']}
                HTTP Status >> {http_status()}
                """
            await ctx.send(embed=discord_embed)
        else:
            embedVar = discord.Embed()
            embedVar.description = f"""
                The query was not successful. 
                
                Debug:
                Success (Player) >> {player['success']}
                Cause (Player) >> {player['cause']}
                HTTP Status >> {http_status()}
                """
            await ctx.send(embed=embedVar)


class hypixel_player_count(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="hypixelcount")
    async def on_message(self, ctx):
        status = player_count()
        if str(status["success"]) == "True":
            embedVar = discord.Embed(title="Games Player Count")
            embedVar.description = f"""
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
            embedVar.add_field(name="HTTP Status",
                               value=http_status, inline=False)
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
            UUID >> {player_statusv3['uuid']}
            Online >> {player_statusv3['session']['online']}
            
            **Success or Not?**
            Success >> {player_statusv3['success']}
            HTTP Status >> {http_status()}
            """
            await ctx.send(embed=embedVar)
        else:
            embedVar = discord.Embed()
            embedVar.description = f"""
            The query was not successful. 

            Debug:
            Success >> {player_statusv3['success']}
            Cause >> {player_statusv3['cause']}
            HTTP Status >> {http_status()}
            """
            await ctx.send(embed=embedVar)


class skywars(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="skywarsinfo")
    async def on_message(self, ctx, *, uuid: str):
        skywars = player_ranked_skywars(uuid)
        if str(skywars["success"]) == "True":
            embedVar = discord.Embed()
            embedVar.description = f"""
            **Skywars Position**
            Position >> {skywars['results']['position']}
            Score >> {skywars['results']['score']}
            
            **Success or Not?**
            Success >> {skywars['success']}
            HTTP Status >> {http_status()}
            """
            await ctx.send(embed=embedVar)
        else:
            embedVar = discord.Embed()
            embedVar.description = f"""
            The query was not successful. 

            Debug:
            Success >> {skywars['success']}
            Cause >> {skywars['cause']}
            HTTP Status >> {http_status()}
            """
            await ctx.send(embed=embedVar)


def setup(bot):
    bot.add_cog(hypixel_api(bot))
    bot.add_cog(hypixel_status(bot))
    bot.add_cog(hypixel_player_count(bot))
    bot.add_cog(skywars(bot))
