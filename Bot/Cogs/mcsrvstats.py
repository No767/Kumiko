import json

import discord
import requests
from discord import Embed
from discord.ext import commands

class mcsrvstats(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name="javamcsrv")
    async def on_message(self, ctx, search: str):
        search = search.replace(" ", "%20")
        link = f"https://api.mcsrvstat.us/2/{search}"
        image_link = f"https://api.mcsrvstat.us/icon/{search}"
        r = requests.get(link)
        mcsrv_data = r.text
        mcsrv = json.loads(mcsrv_data)
        try:
            if "true" == mcsrv['online']:
                embedVar = discord.Embed(color=0xc27c0e)
                embedVar.description = f"""
                **Infomation (Java Edition)**

                Online Status >> {mcsrv['online']}
                Hostname/Domain >> {mcsrv['hostname']}
                IP Address >> {mcsrv['ip']}
                Port >> {mcsrv['port']}

                **Player Count**

                Players Online >> {mcsrv['players']['online']}
                Max Online Player Slots >> {mcsrv['players']['max']}

                **MOTD**

                {mcsrv['motd']['clean']}

                **Debug**
                Ping >> {mcsrv['debug']['ping']}
                Query >> {mcsrv['debug']['query']}
                SRV Record >> {mcsrv['debug']['srv']}
                Query Mismatch >> {mcsrv['debug']['querymismatch']}
                IP in SRV >> {mcsrv['debug']['ipinsrv']}
                CNAME in SRV >> {mcsrv['debug']['cnameinsrv']}
                Animated MOTD >> {mcsrv['debug']['animatedmotd']}
                Cache Time >> {mcsrv['debug']['cachetime']}
                API Version >> {mcsrv['debug']['apiversion']}
                """
                embedVar.set_thumbnail(url=image_link)
                await ctx.send(embed=embedVar)
            else:
                embedVar = discord.Embed(color=0xc27c0e)
                embedVar.description = f"""
                **Infomation (Java Edition)**
            
                Online Status >> {mcsrv['online']}
                Hostname/Domain >> {mcsrv['hostname']}
                IP Address >> {mcsrv['ip']}
                Port >> {mcsrv['port']}
            
                **Debug**
            
                Ping >> {mcsrv['debug']['ping']}
                Query >> {mcsrv['debug']['query']}
                SRV Record >> {mcsrv['debug']['srv']}
                Query Mismatch >> {mcsrv['debug']['querymismatch']}
                IP in SRV >> {mcsrv['debug']['ipinsrv']}
                CNAME in SRV >> {mcsrv['debug']['cnameinsrv']}
                Animated MOTD >> {mcsrv['debug']['animatedmotd']}
                Cache Time >> {mcsrv['debug']['cachetime']}
                """
                embedVar.set_thumbnail(url=image_link)
                await ctx.send(embed=embedVar)
        except:
            embedVar = discord.Embed(color=0xc27c0e)
            embedVar.description = f"""
            Your search for has failed. Please try again.
            """
            await ctx.send(embed=embedVar)

class bedrock_mcsrvstats(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name="bedrockmcsrv")
    async def on_message(self, ctx, search: str):
        search = search.replace(" ", "%20")
        link = f"https://api.mcsrvstat.us/bedrock/2/{search}"
        bedimage_link = f"https://api.mcsrvstat.us/icon/{search}"
        r = requests.get(link)
        bedmcsrv_data = r.text
        bedmcsrv = json.loads(bedmcsrv_data)
        try: 
            if "true" == bedmcsrv["online"]:
                embedVar = discord.Embed(color=0x607d8b)
                embedVar.description = f"""
                **Information (Bedrock Edition)**

                Online Status >> {bedmcsrv['online']}
                Hostname/Domain >> {bedmcsrv['hostname']}
                IP Address >> {bedmcsrv['ip']}
                Port >> {bedmcsrv['port']}
                Supported/Server Version >> {bedmcsrv['version']}
                Map >> {bedmcsrv['map']}

                **Player Count**

                Players Online >> {bedmcsrv['players']['online']}
                Max Online Player Slots >> {bedmcsrv['players']['max']}

                **MOTD**

                {bedmcsrv['motd']['clean']}

                **Debug**

                Protocol >> {bedmcsrv['protocol']}
                Ping >> {bedmcsrv['debug']['ping']}
                Query >> {bedmcsrv['debug']['query']}
                Query Mismatch >> {bedmcsrv['debug']['querymismatch']}
                IP in SRV >> {bedmcsrv['debug']['ipinsrv']}
                CNAME in SRV >> {bedmcsrv['debug']['cnameinsrv']}
                Animated MOTD >> {bedmcsrv['debug']['animatedmotd']}
                Cache Time >> {bedmcsrv['debug']['cachetime']}
                API Version >> {bedmcsrv['debug']['apiversion']}
                """
                embedVar.set_thumbnail(url=bedimage_link)
                await ctx.send(embed=embedVar)
            else:
                embedVar = discord.Embed(color=0x607d8b)
                embedVar.description = f"""
                **Information (Bedrock Edition)**

                Online Status >> {bedmcsrv['online']}
                Hostname/Domain >> {bedmcsrv['hostname']}
                IP Address >> {bedmcsrv['ip']}
                Port >> {bedmcsrv['port']}

                **Debug**

                Ping >> {bedmcsrv['debug']['ping']}
                Query >> {bedmcsrv['debug']['query']}
                SRV Record >> {bedmcsrv['debug']['srv']}
                Query Mismatch >> {bedmcsrv['debug']['querymismatch']}
                IP in SRV >> {bedmcsrv['debug']['ipinsrv']}
                CNAME in SRV >> {bedmcsrv['debug']['cnameinsrv']}
                Animated MOTD >> {bedmcsrv['debug']['animatedmotd']}
                Cache Time >> {bedmcsrv['debug']['cachetime']}
                """
                embedVar.set_thumbnail(url=bedimage_link)
                await ctx.send(embed=embedVar)
        except:
            embedVar = discord.Embed(color=0x607d8b)
            embedVar.description = f"""
            Your search has failed. Please try again.
            """
            await ctx.send(embed=embedVar)
            
def setup(bot):
    bot.add_cog(mcsrvstats(bot))
    bot.add_cog(bedrock_mcsrvstats(bot))