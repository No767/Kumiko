import discord
import requests
import ujson
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
        mcsrv = ujson.loads(r.text)
        mcsrv_status_code = r.status_code
        try:
            if "True" in str(mcsrv["online"]):
                embedVar = discord.Embed(title="Infomation (Java Edition)",color=0xC27C0E)
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

                {str(mcsrv['motd']['clean']).replace("[", "").replace("]", "").replace("'", "")}

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
                HTTP Status (MCSrvStat) >> {mcsrv_status_code}
                """
                embedVar.add_field(name="Online Status", value=mcsrv['online'], inline=True)
                embedVar.add_field(name="Hostname/Domain", value=mcsrv['hostname'], inline=True)
                embedVar.add_field(name="IP Address", value=mcsrv['ip'], inline=True)
                embedVar.add_field(name="Port", value=mcsrv['port'], inline=True)
                embedVar.add_field(name="Players Online", value=mcsrv['players']['online'], inline=True)
                embedVar.add_field(name="Max Online Player Slots", value=mcsrv['players']['max'], inline=True)
                embedVar.add_field(name="MOTD", value=str(mcsrv['motd']['clean']).replace("[", "").replace("]", "").replace("'", ""), inline=True)
                embedVar.add_field(name="Ping", value=mcsrv['debug']['ping'], inline=True)
                embedVar.add_field(name="Query", value=mcsrv['debug']['query'], inline=True)
                embedVar.add_field(name="SRV Record", value=mcsrv['debug']['srv'], inline=True)
                embedVar.add_field(name="Query Mismatch", value=mcsrv['debug']['querymismatch'], inline=True)
                embedVar.add_field(name="IP in SRV", value=mcsrv['debug']['ipinsrv'], inline=True)
                embedVar.add_field(name="CNAME in SRV", value=mcsrv['debug']['cnameinsrv'], inline=True)
                embedVar.add_field(name="Animated MOTD", value=mcsrv['debug']['animatedmotd'], inline=True)
                embedVar.add_field(name="Cache Time", value=mcsrv['debug']['cachetime'], inline=True)
                embedVar.add_field(name="API Version", value=mcsrv['debug']['apiversion'], inline=True)
                embedVar.add_field(name="HTTP Status (MCSrvStat)", value=mcsrv_status_code, inline=True)
                embedVar.set_thumbnail(url=image_link)
                await ctx.send(embed=embedVar)
            else:
                embedVar = discord.Embed(color=0xC27C0E)
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
                HTTP Status (MCSrvStat) >> {mcsrv_status_code}
                """
                embedVar.set_thumbnail(url=image_link)
                await ctx.send(embed=embedVar)
        except Exception as e:
            embedVar = discord.Embed(color=0xC27C0E)
            embedVar.description = f"""
            Your search for has failed. Please try again.\nReason: {e}
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
        bedmcsrv = ujson.loads(r.text)
        bedmcsrv_status_code = r.status_code
        try:
            if "True" in str(bedmcsrv["online"]):
                embedVar = discord.Embed(color=0x607D8B)
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

                {str(bedmcsrv['motd']['clean']).replace("[", "").replace("]", "").replace("'", "")}

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
                HTTP Status (MCSrvStat) >> {bedmcsrv_status_code}
                """
                embedVar.set_thumbnail(url=bedimage_link)
                await ctx.send(embed=embedVar)
            else:
                embedVar = discord.Embed(color=0x607D8B)
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
                HTTP Status (MCSrvStat) >> {bedmcsrv_status_code}
                """
                embedVar.set_thumbnail(url=bedimage_link)
                await ctx.send(embed=embedVar)
        except Exception as e:
            embedVar = discord.Embed(color=0x607D8B)
            embedVar.description = f"""
            Your search has failed. Please try again.\nReason: {e}
            """
            await ctx.send(embed=embedVar)


def setup(bot):
    bot.add_cog(mcsrvstats(bot))
    bot.add_cog(bedrock_mcsrvstats(bot))
