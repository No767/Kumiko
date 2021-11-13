import discord
import requests
import ujson
from discord.ext import commands


class mcsrvstats(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="javamcsrv")
    async def java(self, ctx, search: str):
        search = search.replace(" ", "%20")
        link = f"https://api.mcsrvstat.us/2/{search}"
        image_link = f"https://api.mcsrvstat.us/icon/{search}"
        r = requests.get(link)
        mcsrv = ujson.loads(r.text)
        mcsrv_status_code = r.status_code
        try:
            if "True" in str(mcsrv["online"]):
                embedVar = discord.Embed(
                    title="Infomation (Java Edition)", color=0xC27C0E
                )
                embedVar.add_field(
                    name="Online Status", value=mcsrv["online"], inline=True
                )
                embedVar.add_field(
                    name="Hostname/Domain", value=mcsrv["hostname"], inline=True
                )
                embedVar.add_field(name="IP Address",
                                   value=mcsrv["ip"], inline=True)
                embedVar.add_field(
                    name="Port", value=mcsrv["port"], inline=True)
                embedVar.add_field(
                    name="Players Online", value=mcsrv["players"]["online"], inline=True
                )
                embedVar.add_field(
                    name="Max Online Player Slots",
                    value=mcsrv["players"]["max"],
                    inline=True,
                )
                embedVar.add_field(
                    name="MOTD",
                    value=str(mcsrv["motd"]["clean"])
                    .replace("[", "")
                    .replace("]", "")
                    .replace("'", ""),
                    inline=True,
                )
                embedVar.add_field(
                    name="Ping", value=mcsrv["debug"]["ping"], inline=True
                )
                embedVar.add_field(
                    name="Query", value=mcsrv["debug"]["query"], inline=True
                )
                embedVar.add_field(
                    name="SRV Record", value=mcsrv["debug"]["srv"], inline=True
                )
                embedVar.add_field(
                    name="Query Mismatch",
                    value=mcsrv["debug"]["querymismatch"],
                    inline=True,
                )
                embedVar.add_field(
                    name="IP in SRV", value=mcsrv["debug"]["ipinsrv"], inline=True
                )
                embedVar.add_field(
                    name="CNAME in SRV", value=mcsrv["debug"]["cnameinsrv"], inline=True
                )
                embedVar.add_field(
                    name="Animated MOTD",
                    value=mcsrv["debug"]["animatedmotd"],
                    inline=True,
                )
                embedVar.add_field(
                    name="Cache Time", value=mcsrv["debug"]["cachetime"], inline=True
                )
                embedVar.add_field(
                    name="API Version", value=mcsrv["debug"]["apiversion"], inline=True
                )
                embedVar.add_field(
                    name="HTTP Status (MCSrvStat)", value=mcsrv_status_code, inline=True
                )
                embedVar.set_thumbnail(url=image_link)
                await ctx.send(embed=embedVar)
            else:
                embedVar = discord.Embed(title="Infomation (Java Edition)", color=0xC27C0E)
                embedVar.add_field(name="Online Status", value=mcsrv["online"])
                embedVar.add_field(
                    name="Hostname/Domain", value=mcsrv["hostname"], inline=True
                )
                embedVar.add_field(name="IP Address",
                                   value=mcsrv["ip"], inline=True)
                embedVar.add_field(
                    name="Port", value=mcsrv["port"], inline=True)
                embedVar.add_field(
                    name="Ping", value=mcsrv["debug"]["ping"], inline=True
                )
                embedVar.add_field(
                    name="Query", value=mcsrv["debug"]["query"], inline=True
                )
                embedVar.add_field(
                    name="SRV Record", value=mcsrv["debug"]["srv"], inline=True
                )
                embedVar.add_field(
                    name="Query Mismatch",
                    value=mcsrv["debug"]["querymismatch"],
                    inline=True,
                )
                embedVar.add_field(
                    name="IP in SRV", value=mcsrv["debug"]["ipinsrv"], inline=True
                )
                embedVar.add_field(
                    name="CNAME in SRV", value=mcsrv["debug"]["cnameinsrv"], inline=True
                )
                embedVar.add_field(
                    name="Animated MOTD",
                    value=mcsrv["debug"]["animatedmotd"],
                    inline=True,
                )
                embedVar.add_field(
                    name="Cache Time", value=mcsrv["debug"]["cachetime"], inline=True
                )
                embedVar.add_field(
                    name="HTTP Status (MCSrvStat)", value=mcsrv_status_code, inline=True
                )
                embedVar.set_thumbnail(url=image_link)
                await ctx.send(embed=embedVar)
        except Exception as e:
            embedVar = discord.Embed(color=0xC27C0E)
            embedVar.description = f"Your search for has failed. Please try again.\nReason: {e}"
            await ctx.send(embed=embedVar)

    @java.error
    async def on_message_error(
        self, ctx: commands.Context, error: commands.CommandError
    ):
        if isinstance(error, commands.MissingRequiredArgument):
            embedVar = discord.Embed(color=discord.Color.from_rgb(255, 51, 51))
            embedVar.description = f"Missing a required argument: {error.param}"
            msg = await ctx.send(embed=embedVar, delete_after=10)
            await msg.delete(delay=10)

class bedrock_mcsrvstats(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="bedrockmcsrv")
    async def bedrock(self, ctx, search: str):
        search = search.replace(" ", "%20")
        link = f"https://api.mcsrvstat.us/bedrock/2/{search}"
        bedimage_link = f"https://api.mcsrvstat.us/icon/{search}"
        r = requests.get(link)
        bedmcsrv = ujson.loads(r.text)
        bedmcsrv_status_code = r.status_code
        try:
            if "True" in str(bedmcsrv["online"]):
                embedVar = discord.Embed(title="Information (Bedrock Edition)", color=0x607D8B)
                embedVar.add_field(name="Online Status", value=bedmcsrv['online'], inline=True)
                embedVar.add_field(name="Hostname/Domain", value=bedmcsrv['hostname'], inline=True)
                embedVar.add_field(name="IP Address", value=bedmcsrv['ip'], inline=True)
                embedVar.add_field(name="Port", value=bedmcsrv['port'], inline=True)
                embedVar.add_field(name="Supported/Server Version", value=bedmcsrv['version'], inline=True)
                embedVar.add_field(name="Map", value=bedmcsrv['map'], inline=True)
                embedVar.add_field(name="Players Online", value=bedmcsrv['players']['online'], inline=True)
                embedVar.add_field(name="Max Online Player Slots", value=bedmcsrv['players']['max'], inline=True)
                embedVar.add_field(name="MOTD", value=str(bedmcsrv['motd']['clean']).replace("[", "").replace("]", "").replace("'", ""), inline=True)
                embedVar.add_field(name="Protocol", value=bedmcsrv['protocol'], inline=True)
                embedVar.add_field(name="Ping", value=bedmcsrv['debug']['ping'], inline=True)
                embedVar.add_field(name="Query", value=bedmcsrv['debug']['query'], inline=True)
                embedVar.add_field(name="Query Mismatch", value=bedmcsrv['debug']['query_mismatch'], inline=True)
                embedVar.add_field(name="IP in SRV", value=bedmcsrv['debug']['ipinsrv'], inline=True)
                embedVar.add_field(name="CNAME in SRV", value=bedmcsrv['debug']['cnameinsrv'], inline=True)
                embedVar.add_field(name="Animated MOTD", value=bedmcsrv['debug']['animatedmotd'], inline=True)
                embedVar.add_field(name="Cache Time", value=bedmcsrv['debug']['cachetime'], inline=True)
                embedVar.add_field(name="API Version", value=bedmcsrv['debug']['apiversion'], inline=True)
                embedVar.add_field(name="HTTP Status (MCSrvStat)", value=bedmcsrv_status_code, inline=True)
                embedVar.set_thumbnail(url=bedimage_link)
                await ctx.send(embed=embedVar)
            else:
                embedVar = discord.Embed(title="Information (Bedrock Edition)", color=0x607D8B)
                embedVar.add_field(name="Online Status", value=bedmcsrv['online'], inline=True)
                embedVar.add_field(name="Hostname/Domain", value=bedmcsrv['hostname'], inline=True)
                embedVar.add_field(name="IP Address", value=bedmcsrv['ip'], inline=True)
                embedVar.add_field(name="Port", value=bedmcsrv['port'], inline=True)
                embedVar.add_field(name="Ping", value=bedmcsrv['debug']['ping'], inline=True)
                embedVar.add_field(name="Query", value=bedmcsrv['debug']['query'], inline=True)
                embedVar.add_field(name="Query Mismatch", value=bedmcsrv['debug']['query_mismatch'], inline=True)
                embedVar.add_field(name="IP in SRV", value=bedmcsrv['debug']['ipinsrv'], inline=True)
                embedVar.add_field(name="CNAME in SRV", value=bedmcsrv['debug']['cnameinsrv'], inline=True)
                embedVar.add_field(name="Animated MOTD", value=bedmcsrv['debug']['animatedmotd'], inline=True)
                embedVar.add_field(name="Cache Time", value=bedmcsrv['debug']['cachetime'], inline=True)
                embedVar.add_field(name="HTTP Status (MCSrvStat)", value=bedmcsrv_status_code, inline=True)
                embedVar.set_thumbnail(url=bedimage_link)
                await ctx.send(embed=embedVar)
        except Exception as e:
            embedVar = discord.Embed(color=0x607D8B)
            embedVar.description = f"Your search has failed. Please try again.\nReason: {e}"
            await ctx.send(embed=embedVar)
            
    @bedrock.error
    async def on_message_error(
        self, ctx: commands.Context, error: commands.CommandError
    ):
        if isinstance(error, commands.MissingRequiredArgument):
            embedVar = discord.Embed(color=discord.Color.from_rgb(255, 51, 51))
            embedVar.description = f"Missing a required argument: {error.param}"
            msg = await ctx.send(embed=embedVar, delete_after=10)
            await msg.delete(delay=10)

def setup(bot):
    bot.add_cog(mcsrvstats(bot))
    bot.add_cog(bedrock_mcsrvstats(bot))
