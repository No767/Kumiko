import typing

import discord
import discord.ext
from discord.ext import commands


class rinhelp(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.last_member = None

    @commands.command(name="rinhelp", help="Rin's Help/Info Page")
    async def on_message(self, ctx, *, search: typing.Optional[str] = None):
        try:
            if search is None:
                bot = self.bot
                embedVar = discord.Embed(color=14414079)
                embedVar.description = """
                        **[GitHub](https://github.com/No767/Rin)** | **[Docs](https://rin-docs.readthedocs.io/en/latest/)** | **Invite**
                        """
                embedVar.add_field(
                    name="Admin", value="`.rinhelp admin`", inline=True)
                embedVar.add_field(
                    name="Twitter", value="`.rinhelp twitter`", inline=True
                )
                embedVar.add_field(
                    name="Reddit", value="`.rinhelp reddit`", inline=True
                )
                embedVar.add_field(
                    name="Minecraft", value="`.rinhelp mc`", inline=True)
                embedVar.add_field(
                    name="Fun", value="`.rinhelp fun`", inline=True)
                embedVar.add_field(
                    name="Instagram", value="`.rinhelp ig`", inline=True)
                embedVar.add_field(
                    name="Chat", value="`.rinhelp chat`", inline=True)
                embedVar.add_field(
                    name="Misc", value="`.rinhelp misc`", inline=True)
                embedVar.add_field(
                    name="Deviantart", value="`.rinhelp da`", inline=True
                )
                embedVar.add_field(
                    name="Anime", value="`.rinhelp anime`", inline=True)
                embedVar.set_author(
                    name="Rin Help", icon_url=bot.user.avatar_url)
                embedVar.set_footer(
                    text='Remember, the command prefix for this bot is "."'
                )
                await ctx.send(embed=embedVar)

            if str(search) == "admin":
                bot = self.bot
                embedVar = discord.Embed(color=14414079)
                embedVar.add_field(
                    name="`botgrowth`",
                    value="Tips based on bot statistics on how to reach more people!",
                    inline=True,
                )
                embedVar.add_field(
                    name="`prune`",
                    value="Removes bot from servers smaller than the specified limit\n",
                    inline=True,
                )
                embedVar.add_field(
                    name="`botinfo`", value="Statistics about this bot", inline=True
                )
                embedVar.add_field(
                    name="`serverinfo`", value="Known server information", inline=True
                )
                embedVar.add_field(
                    name="`ping`", value="Checks the ping for the bot", inline=True
                )
                embedVar.add_field(
                    name="`ban`", value="Bans the specified user", inline=True
                )
                embedVar.set_author(
                    name="Rin Help - Admin", icon_url=bot.user.avatar_url
                )
                await ctx.send(embed=embedVar)

            if str(search) == "twitter":
                bot = self.bot
                embedVar = discord.Embed(color=14414079)
                embedVar.add_field(
                    name="`rt`", value="Grabs Twitter user's timeline", inline=True
                )
                embedVar.add_field(
                    name="`rtupdatestatus`",
                    value="Updates Twitter user's status",
                    inline=True,
                )
                embedVar.add_field(
                    name="`rtsearch`", value="Searches for twitter users", inline=True
                )
                embedVar.set_author(
                    name="Rin Help - Twitter", icon_url=bot.user.avatar_url
                )
                embedVar.set_footer(
                    text="Note: Currently the Twitter Cog is broken. Reworking it soon"
                )
                await ctx.send(embed=embedVar)

            if str(search) == "reddit":
                bot = self.bot
                embedVar = discord.Embed(color=14414079)
                embedVar.add_field(
                    name="`reddit`", value="searches on reddit", inline=True
                )
                embedVar.add_field(
                    name="`transmeme`",
                    value="searches on reddit that include trans and other LGBTQ+ subreddits",
                    inline=True,
                )
                embedVar.add_field(
                    name="`meme`",
                    value="searches on reddit that include defined search topics regarding memes",
                    inline=True,
                )
                embedVar.set_author(
                    name="Rin Help - Reddit", icon_url=bot.user.avatar_url
                )
                await ctx.send(embed=embedVar)

            if str(search) in ("minecraft", "mc"):
                bot = self.bot
                embedVar = discord.Embed(color=14414079)
                embedVar.add_field(
                    name="`javamcsrv`", value="Obtains Java server status", inline=True
                )
                embedVar.add_field(
                    name="`bedrockmcsrv`",
                    value="Obtains bedrock server status",
                    inline=True,
                )
                embedVar.add_field(
                    name="`hypixel`",
                    value="Gain Insight in Hypixel's player data",
                    inline=True,
                )
                embedVar.add_field(
                    name="`hypixelcount`",
                    value="Obtain the amount of players online within the servers",
                    inline=True,
                )
                embedVar.add_field(
                    name="`hypixelplayerstatus`",
                    value="Determine if the player requests is online or " "not",
                    inline=True,
                )
                embedVar.add_field(
                    name="`skywarsinfo`",
                    value="Get the position and score of the player within "
                    "**ranked** skywars",
                    inline=True,
                )
                embedVar.add_field(
                    name="`spiget-search`",
                    value="Searches for Minecraft plugins via Spiget and returns information on such plugin",
                    inline=True,
                )
                embedVar.add_field(
                    name="`spiget-author`",
                    value="Searches for given author and returns name and resources from the author",
                    inline=True,
                )
                embedVar.add_field(
                    name="`spiget-stats`",
                    value="Returns stats for Spiget (total resources created, etc)",
                    inline=True,
                )
                embedVar.add_field(
                    name="`spiget-status`",
                    value="Returns HTTP Status of the Spiget API",
                    inline=True,
                )
                embedVar.set_author(
                    name="Rin Help - Minecraft", icon_url=bot.user.avatar_url
                )
                await ctx.send(embed=embedVar)

            if str(search) == "fun":
                bot = self.bot
                embedVar = discord.Embed(color=14414079)
                embedVar.add_field(
                    name="`pinger`",
                    value="Annoys everyone with a message and allows for how much that message is sent for",
                    inline=True,
                )
                embedVar.add_field(
                    name="`valid`", value="Provides some valid feedback", inline=True
                )
                embedVar.add_field(
                    name="`mylvl`", value="Displays DisQuest Level", inline=True
                )
                embedVar.add_field(
                    name="`image`", value="Scraps Images on Deviantart", inline=True
                )
                embedVar.add_field(
                    name="`rank`",
                    value="Displays the most active members of your server",
                    inline=True,
                )
                embedVar.add_field(
                    name="`globalrank`",
                    value="Displays the most active members of all servers that this bot is connected to",
                    inline=True,
                )
                embedVar.add_field(
                    name="`advice`",
                    value="Returns some advice from Advice Slip",
                    inline=True,
                )
                embedVar.set_author(name="Rin Help - Fun",
                                    icon_url=bot.user.avatar_url)
                await ctx.send(embed=embedVar)

            if str(search) in ("instagram", "ig"):
                bot = self.bot
                embedVar = discord.Embed(color=14414079)
                embedVar.add_field(
                    name="`iguserinfo`",
                    value="Uses the User's Client ID in order to obtain Instagram User Info",
                    inline=True,
                )
                embedVar.add_field(
                    name="`igusersearch`",
                    value="Searches for users on Instagram",
                    inline=True,
                )
                embedVar.add_field(
                    name="`igtaginfo`", value="Obtains Tag Info", inline=True
                )
                embedVar.add_field(
                    name="`igusernamecheck`",
                    value="Checks if the specified username is taken or not",
                    inline=True,
                )
                embedVar.set_footer(
                    text="Note: Instagram likes to rate limit users like me with their private API. Make sure not to send too much requests, or else this cog will not work. A cooldown system is being worked on to address this issue."
                )
                embedVar.set_author(
                    name="Rin Help - Instagram", icon_url=bot.user.avatar_url
                )
                await ctx.send(embed=embedVar)

            if str(search) == "chat":
                bot = self.bot
                embedVar = discord.Embed(color=14414079)
                embedVar.add_field(
                    name="`chathelp`",
                    value="The chat is automatically generated based on prewritten responses. Responses that are not documented will be ignored",
                    inline=True,
                )
                embedVar.add_field(
                    name="`clear`",
                    value="Clears number of messages specified from the channel in which int he command was called",
                )
                embedVar.add_field(
                    name="`mute`", value="Mutes that specified user", inline=True
                )
                embedVar.set_author(
                    name="Rin Help - Chat", icon_url=bot.user.avatar_url
                )
                await ctx.send(embed=embedVar)

            if str(search) == "misc":
                bot = self.bot
                embedVar = discord.Embed(color=14414079)
                embedVar.add_field(
                    name="`jisho`",
                    value="Uses Jisho and JMDict in order to obtain info on a word in Japanese",
                    inline=True,
                )
                embedVar.add_field(
                    name="`translate`",
                    value="Translates the given message. Note that as of now, it's only set to english",
                    inline=True,
                )
                embedVar.add_field(
                    name="`rinhelp`", value="Rin's Help command", inline=True
                )
                embedVar.set_author(
                    name="Rin Help - Misc", icon_url=bot.user.avatar_url
                )
                await ctx.send(embed=embedVar)

            if str(search) in ("deviantart", "da"):
                bot = self.bot
                embedVar = discord.Embed(color=14414079)
                embedVar.add_field(
                    name="`devartfind`", value="Finds art on DeviantArt", inline=True
                )
                embedVar.add_field(
                    name="`devartsearch`", value="Search for art", inline=True
                )
                embedVar.add_field(
                    name="`devartuserget`",
                    value="Obtains info on a user on DeviantArt",
                    inline=True,
                )
                embedVar.set_footer(
                    text="Note: currently this feature is broken")
                embedVar.set_author(
                    name="Rin Help - Deviantart", icon_url=bot.user.avatar_url
                )
                await ctx.send(embed=embedVar)
            if str(search) == "anime":
                bot = self.bot
                embedVar = discord.Embed(color=14414079)
                embedVar.add_field(
                    name="`waifu`",
                    value="Randomly selects a waifu from MyWaifuList",
                    inline=True,
                )
                embedVar.add_field(
                    name="`waifupics`",
                    value="Search for art from Waifu.pics",
                    inline=True,
                )
                embedVar.add_field(
                    name="`jikan-search`",
                    value="Searches on Jikan/MAL and returns info about yourselected anime",
                    inline=True,
                )
                embedVar.set_author(
                    name="Rin Help - Anime", icon_url=bot.user.avatar_url
                )
                await ctx.send(embed=embedVar)
        except Exception as e:
            bot = self.bot
            embedVar = discord.Embed(title="Rin Help", color=14414079)
            embedVar.description = f"The query failed.\nReason: {e}"
            embedVar.set_thumbnail(url=bot.user.avatar_url)
            await ctx.send(embed=embedVar)


def setup(bot):
    bot.add_cog(rinhelp(bot))
