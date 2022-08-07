import asyncio

import discord
import discord.ext
import uvloop
from discord.commands import Option, slash_command
from discord.ext import commands


class rinhelp(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.last_member = None

    @slash_command(
        name="help",
        description="The Help Page for Rin",
    )
    async def rinHelp(
        self,
        ctx,
        *,
        category: Option(
            str,
            "The different categories of services that Rin offers",
            choices=[
                "AdviceSlip",
                "AniList",
                "Blue-Alliance",
                "Discord.bots.gg",
                "First-FRC",
                "GitHub",
                "Hypixel",
                "Jisho",
                "MangaDex",
                "Minecraft",
                "Misc",
                "Modrinth",
                "MyAnimeList",
                "Reddit",
                "Spigot",
                "Tenor",
                "Top.gg",
                "Twitch",
                "Twitter",
                "Waifu",
                "YouTube",
            ],
            required=False,
        )
    ):
        try:
            if category is None:
                bot = self.bot
                embedVar = discord.Embed(color=14414079)
                view = discord.ui.View(timeout=None)
                embedVar.add_field(
                    name="AdviceSlip", value="`/help AdviceSlip`", inline=True
                )
                embedVar.add_field(name="AniList", value="`/help AniList`", inline=True)
                embedVar.add_field(
                    name="Blue Alliance", value="`/help Blue-Alliance`", inline=True
                )
                embedVar.add_field(
                    name="First FRC", value="`/help First-FRC`", inline=True
                )
                embedVar.add_field(name="GitHub", value="`/help GitHub`", inline=True)
                embedVar.add_field(name="Hypixel", value="`/help Hypixel`", inline=True)
                embedVar.add_field(name="Jisho", value="`/help Jisho`", inline=True)
                embedVar.add_field(
                    name="MangaDex", value="`/help MangaDex`", inline=True
                )
                embedVar.add_field(
                    name="Minecraft", value="`/help Minecraft`", inline=True
                )
                embedVar.add_field(name="Misc", value="`/help Misc`", inline=True)
                embedVar.add_field(
                    name="Modrinth", value="`/help Modrinth`", inline=True
                )
                embedVar.add_field(
                    name="MyAnimeList", value="`/help MyAnimeList`", inline=True
                )
                embedVar.add_field(name="Reddit", value="`/help Reddit`", inline=True)
                embedVar.add_field(name="Spigot", value="`/help Spigot`", inline=True)
                embedVar.add_field(name="Tenor", value="`/help Tenor`", inline=True)
                embedVar.add_field(name="Top.gg", value="`/help Topgg`", inline=True)
                embedVar.add_field(name="Twitter", value="`/help Twitch`", inline=True)
                embedVar.add_field(name="Twitter", value="`/help Twitter`", inline=True)
                embedVar.add_field(name="Waifu", value="`/help Waifu`", inline=True)
                embedVar.add_field(name="YouTube", value="`/help YouTube`", inline=True)
                embedVar.set_author(
                    name="Help",
                    url=discord.Embed.Empty,
                    icon_url=bot.user.display_avatar,
                )
                embedVar.set_footer(
                    text='Remember, the command prefix for this bot is "/"'
                )
                view.add_item(
                    discord.ui.Button(
                        label="GitHub", url="https://github.com/No767/Rin"
                    )
                )
                view.add_item(
                    discord.ui.Button(label="Docs", url="https://docs.rinbot.live")
                )
                view.add_item(
                    discord.ui.Button(
                        label="Invite",
                        url="https://top.gg/bot/865883525932253184/invite",
                    )
                )
                view.add_item(
                    discord.ui.Button(label="Website", url="https://rinbot.live")
                )
                await ctx.respond(embed=embedVar, view=view)

            if category in ["AdviceSlip"]:
                bot = self.bot
                embedVar = discord.Embed(color=14414079)
                embedVar.add_field(
                    name="`advice`",
                    value="Gives some advice from AdviceSlip",
                    inline=True,
                )
                embedVar.set_author(
                    name="Help - AdviceSlip", icon_url=bot.user.display_avatar
                )
                await ctx.respond(embed=embedVar)

            if category in ["AniList"]:
                bot = self.bot
                embedVar = discord.Embed(color=14414079)
                embedVar.description = "Base command: `anilist`"
                embedVar.add_field(
                    name="`search anime`",
                    value="Searches up to 25 animes on AniList",
                    inline=True,
                )
                embedVar.add_field(
                    name="`search manga`",
                    value="Searches up to 25 mangas on AniList",
                    inline=True,
                )
                embedVar.add_field(
                    name="`search tags`",
                    value="Searches up to 25 tags on AniList",
                    inline=True,
                )
                embedVar.add_field(
                    name="`search users`",
                    value="Searches up to 25 users on AniList",
                    inline=True,
                )
                embedVar.add_field(
                    name="`search characters`",
                    value="Searches up to 25 characters on AniList",
                    inline=True,
                )
                embedVar.add_field(
                    name="`search actors`",
                    value="Searches up to 25 actors on AniList",
                    inline=True,
                )
                embedVar.set_author(
                    name="Help - AniList", icon_url=bot.user.display_avatar
                )
                await ctx.respond(embed=embedVar)

            if category in ["Blue-Alliance"]:
                bot = self.bot
                embedVar = discord.Embed(color=14414079)
                embedVar.description = "Base command: `blue-alliance`"
                embedVar.add_field(
                    name="`matches team`",
                    value="Returns the general info for each match that a team was in during the given event",
                    inline=True,
                )
                embedVar.add_field(
                    name="`matches all`",
                    value="Returns all of the matches for an FRC event",
                    inline=True,
                )
                embedVar.add_field(
                    name="`teams info`",
                    value="Returns info about an FRC team",
                    inline=True,
                )
                embedVar.add_field(
                    name="`teams events`",
                    value="Returns what events an FRC team as attended",
                    inline=True,
                )
                embedVar.add_field(
                    name="`rankings`", value="Returns the event ranking of an event"
                )
                embedVar.set_author(
                    name="Help - Blue Alliance", icon_url=bot.user.display_avatar
                )
                await ctx.respond(embed=embedVar)

            if category in ["Discord.bots.gg"]:
                bot = self.bot
                embedVar = discord.Embed(color=14414079)
                embedVar.description = "Base command: `discordbots`"
                embedVar.add_field(
                    name="`search bots`",
                    value="Searches for any Discord bots listed on discord.bots.gg",
                    inline=True,
                )
                embedVar.set_author(
                    name="Help - Discord.bots.gg", icon_url=bot.user.display_avatar
                )
                await ctx.respond(embed=embedVar)

            if category in ["First-FRC"]:
                bot = self.bot
                embedVar = discord.Embed(color=14414079)
                embedVar.description = "Base command: `frc`"
                embedVar.add_field(
                    name="`events list`",
                    value="Returns events for the current FRC season",
                    inline=True,
                )
                embedVar.add_field(
                    name="`events top`",
                    value="Returns the top 10 FRC teams within a given event",
                    inline=True,
                )
                embedVar.add_field(
                    name="`events schedule`",
                    value="Returns the schedule for a given event",
                    inline=True,
                )
                embedVar.add_field(
                    name="`events alliances`",
                    value="Returns the alliances within a given event",
                    inline=True,
                )
                embedVar.add_field(
                    name="`season`",
                    value="Returns the seasons summary for the current FRC season (may cause spam)",
                    inline=True,
                )
                embedVar.add_field(
                    name="`score`",
                    value="Returns the score for a given team",
                    inline=True,
                )
                embedVar.add_field(
                    name="`results`",
                    value="Returns the FRc team's results for a given event",
                    inline=True,
                )
                embedVar.set_author(
                    name="Help - First-FRC", icon_url=bot.user.display_avatar
                )
                await ctx.respond(embed=embedVar)

            if category in ["GitHub"]:
                bot = self.bot
                embedVar = discord.Embed(color=14414079)
                embedVar.description = "Base command: `github`"
                embedVar.add_field(
                    name="`user one`",
                    value="Returns the user's profile on GitHub",
                    inline=True,
                )
                embedVar.add_field(
                    name="`search repos`",
                    value="Searches for repos on GitHub",
                    inline=True,
                )
                embedVar.add_field(
                    name="`search users`",
                    value="Searches for users on GitHub",
                    inline=True,
                )
                embedVar.add_field(
                    name="`issues all`",
                    value="Gets all issues from a repo",
                    inline=True,
                )
                embedVar.add_field(
                    name="`issues one`",
                    value="Gets info about one issue on any repo on GitHub",
                    inline=True,
                )
                embedVar.add_field(
                    name="`releases list`",
                    value="Lists out up to 25 releases of any repo",
                    inline=True,
                )
                embedVar.add_field(
                    name="`releases latest`",
                    value="Gets the latest published full release for any repo",
                    inline=True,
                )
                embedVar.add_field(
                    name="`repo`",
                    value="Gets info about a repo based on repo name",
                    inline=True,
                )
                embedVar.set_author(
                    name="Help - GitHub", icon_url=bot.user.display_avatar
                )
                await ctx.respond(embed=embedVar)

            if category in ["Hypixel"]:
                bot = self.bot
                embedVar = discord.Embed(color=14414079)
                embedVar.description = "Base command: `hypixel`"
                embedVar.add_field(
                    name="`count`",
                    value="Returns the amount of players in each game server",
                    inline=True,
                )
                embedVar.add_field(
                    name="`punishments`",
                    value="Shows the stats for the amount of punishments given on Hypixel (All Users)",
                    inline=True,
                )
                embedVar.set_author(
                    name="Help - Hypixel", icon_url=bot.user.display_avatar
                )
                await ctx.respond(embed=embedVar)

            if category in ["Jisho"]:
                bot = self.bot
                embedVar = discord.Embed(color=14414079)
                embedVar.add_field(
                    name="`jisho`",
                    value="Searches for any words and/or definitions on Jisho",
                    inline=True,
                )
                embedVar.set_author(
                    name="Help - Jisho", icon_url=bot.user.display_avatar
                )
                await ctx.respond(embed=embedVar)

            if category in ["MangaDex"]:
                bot = self.bot
                embedVar = discord.Embed(color=14414079)
                embedVar.description = "Base command: `mangadex`"
                embedVar.add_field(
                    name="`search scanlation`",
                    value="Returns up to 5 scanlation groups via the name given",
                    inline=True,
                )
                embedVar.add_field(
                    name="`search manga`",
                    value="Searches for up to 5 manga on MangaDex",
                    inline=True,
                )
                embedVar.add_field(
                    name="`search author`",
                    value="Returns up to 5 authors and their info",
                    inline=True,
                )
                embedVar.add_field(
                    name="`random`",
                    value="Returns an random manga from MangaDex",
                    inline=True,
                )
                embedVar.set_author(
                    name="Help - MangaDex", icon_url=bot.user.display_avatar
                )
                await ctx.respond(embed=embedVar)

            if category in ["Minecraft"]:
                bot = self.bot
                embedVar = discord.Embed(color=14414079)
                embedVar.description = "Base command: `minecraft`"
                embedVar.add_field(
                    name="`java`",
                    value="Checks and returns info about the given Minecraft Java server",
                    inline=True,
                )
                embedVar.add_field(
                    name="`bedrock`",
                    value="Returns the status and info of any Bedrock or Geyser-compatible server",
                    inline=True,
                )
                embedVar.set_author(
                    name="Help - Minecraft", icon_url=bot.user.display_avatar
                )
                await ctx.respond(embed=embedVar)

            if category in ["Misc"]:
                bot = self.bot
                embedVar = discord.Embed(color=14414079)
                embedVar.add_field(
                    name="`botinfo`", value="Returns stats for Rin", inline=True
                )
                embedVar.add_field(
                    name="`help`", value="The help page for Rin", inline=True
                )
                embedVar.add_field(
                    name="`ping`", value="Returns the ping of Rin", inline=True
                )
                embedVar.add_field(name="`info`", value="Info about Rin", inline=True)
                embedVar.add_field(
                    name="`invite`", value="Invite links for Rin", inline=True
                )
                embedVar.add_field(
                    name="`uptime`", value="Returns the uptime of Rin", inline=True
                )
                embedVar.add_field(
                    name="`version`", value="Returns the version of Rin", inline=True
                )
                embedVar.set_author(
                    name="Help - Misc", icon_url=bot.user.display_avatar
                )
                await ctx.respond(embed=embedVar)

            if category in ["Modrinth"]:
                bot = self.bot
                embedVar = discord.Embed(color=14414079)
                embedVar.description = "Base command: `modrinth`"
                embedVar.add_field(
                    name="`mod list`",
                    value="Gets info about the mod requested",
                    inline=True,
                )
                embedVar.add_field(
                    name="`versions all`",
                    value="Lists out all of the versions for a mod",
                    inline=True,
                )
                embedVar.add_field(
                    name="`users search`",
                    value="Returns info on the given user",
                    inline=True,
                )
                embedVar.add_field(
                    name="`users projects`",
                    value="Returns info on the given user's projects",
                    inline=True,
                )
                embedVar.add_field(
                    name="`search`", value="Searches for up to 5 mods on Modrinth"
                )
                embedVar.set_author(
                    name="Help - Modrinth", icon_url=bot.user.display_avatar
                )
                await ctx.respond(embed=embedVar)

            if category in ["MyAnimeList"]:
                bot = self.bot
                embedVar = discord.Embed(color=14414079)
                embedVar.description = "Base command: `mal`"
                embedVar.add_field(
                    name="`seasons list`",
                    value="Returns animes for the given season and year",
                    inline=True,
                )
                embedVar.add_field(
                    name="`seasons upcoming`",
                    value="Returns anime for the upcoming season",
                    inline=True,
                )
                embedVar.add_field(
                    name="`random anime`", value="Fetches a random anime from MAL"
                )
                embedVar.add_field(
                    name="`random manga`",
                    value="Fetches a random manga from MAL",
                    inline=True,
                )
                embedVar.add_field(
                    name="`search anime`",
                    value="Fetches up to 5 anime from MAL",
                    inline=True,
                )
                embedVar.add_field(
                    name="`search manga`",
                    value="Fetches up to 5 manga from MAL",
                    inline=True,
                )
                embedVar.add_field(
                    name="`user`",
                    value="Fetches the user's profile from MAL",
                    inline=True,
                )
                embedVar.set_author(
                    name="Help - MyAnimeList", icon_url=bot.user.display_avatar
                )
                await ctx.respond(embed=embedVar)

            if category in ["Reddit"]:
                bot = self.bot
                embedVar = discord.Embed(color=14414079)
                embedVar.description = "Base command: `reddit`"
                embedVar.add_field(
                    name="`users info`",
                    value="Provides info about a Redditor",
                    inline=True,
                )
                embedVar.add_field(
                    name="`users comments`",
                    value="Returns up to 10 comments from a given Redditor",
                    inline=True,
                )
                embedVar.add_field(
                    name="`search`", value="Searches on reddit for content", inline=True
                )
                embedVar.add_field(
                    name="`feed`",
                    value="Returns up to 25 reddit posts based on the current filter",
                    inline=True,
                )
                embedVar.add_field(
                    name="`egg_irl`",
                    value="Literally just shows you r/egg_irl posts. This was made just for fun.",
                    inline=True,
                )
                embedVar.set_author(
                    name="Help - Reddit", icon_url=bot.user.display_avatar
                )
                await ctx.respond(embed=embedVar)

            if category in ["Spigot"]:
                bot = self.bot
                embedVar = discord.Embed(color=14414079)
                embedVar.description = "Base command: `spigot`"
                embedVar.add_field(
                    name="`search`",
                    value="Finds up to 25 plugins matching the name of the given plugin",
                    inline=True,
                )
                embedVar.set_author(
                    name="Help - Spigot", icon_url=bot.user.display_avatar
                )
                await ctx.respond(embed=embedVar)

            if category in ["Tenor"]:
                bot = self.bot
                embedVar = discord.Embed(color=14414079)
                embedVar.description = "Base command: `tenor`"
                embedVar.add_field(
                    name="`search multiple`",
                    value="Searches for a single gif on Tenor",
                    inline=True,
                )
                embedVar.add_field(
                    name="`search one`",
                    value="Searches for a single gif on Tenor",
                    inline=True,
                )
                embedVar.add_field(
                    name="`search suggestions`",
                    value="Gives a list of suggested search terms based on the given topic",
                    inline=True,
                )
                embedVar.add_field(
                    name="`featured`",
                    value="Returns up to 25 featured gifs from Tenor",
                    inline=True,
                )
                embedVar.add_field(
                    name="`trending terms`",
                    value="Returns a list of trending search terms",
                    inline=True,
                )
                embedVar.add_field(
                    name="`random`",
                    value="Gives out 25 random gifs from Tenor based on the given search term",
                    inline=True,
                )
                embedVar.set_author(
                    name="Help - Tenor", icon_url=bot.user.display_avatar
                )
                await ctx.respond(embed=embedVar)

            if category in ["Top.gg"]:
                bot = self.bot
                embedVar = discord.Embed(color=14414079)
                embedVar.description = "Base command: `topgg`"
                embedVar.add_field(
                    name="`search bot`",
                    value="Searches for a bot on Top.gg",
                    inline=True,
                )
                embedVar.set_author(
                    name="Help - Top.gg", icon_url=bot.user.display_avatar
                )
                await ctx.respond(embed=embedVar)

            if category in ["Twitch"]:
                bot = self.bot
                embedVar = discord.Embed(color=14414079)
                embedVar.description = "Base command: `twitch`"
                embedVar.add_field(
                    name="`search channels`",
                    value="Returns up to 25 streams from the given channel",
                    inline=True,
                )
                embedVar.add_field(
                    name="`streams`",
                    value="Gets up to 25 active streams on Twitch",
                    inline=True,
                )
                embedVar.add_field(
                    name="`top games`",
                    value="Gets the top 100 games on Twitch",
                    inline=True,
                )
                embedVar.set_author(
                    name="Help - Twitch", icon_url=bot.user.display_avatar
                )
                await ctx.respond(embed=embedVar)

            if category in ["Twitter"]:
                bot = self.bot
                embedVar = discord.Embed(color=14414079)
                embedVar.description = "Base command: `twitter`"
                embedVar.add_field(
                    name="`search`",
                    value="Returns up to 5 recent tweets from the given twitter user",
                    inline=True,
                )
                embedVar.add_field(
                    name="`user`",
                    value="Returns the user's profile from Twitter",
                    inline=True,
                )
                embedVar.set_author(
                    name="Help - Twitter", icon_url=bot.user.display_avatar
                )
                await ctx.respond(embed=embedVar)

            if category in ["Waifu"]:
                bot = self.bot
                embedVar = discord.Embed(color=14414079)
                embedVar.description = "Base command: `waifu`"
                embedVar.add_field(
                    name="`random one`",
                    value="Gets one random waifu pics",
                    inline=True,
                )
                embedVar.add_field(
                    name="`random many`",
                    value="Returns many random waifu pics",
                    inline=True,
                )
                embedVar.add_field(
                    name="`pics`",
                    value="Returns a random image of a waifu from waifu.pics",
                    inline=True,
                )
                embedVar.set_author(
                    name="Help - Waifu", icon_url=bot.user.display_avatar
                )
                await ctx.respond(embed=embedVar)
            if category in ["YouTube"]:
                bot = self.bot
                embedVar = discord.Embed(color=14414079)
                embedVar.description = "Base command: `youtube`"
                embedVar.add_field(
                    name="`search`",
                    value="Returns up to 5 videos from the given YouTube search term",
                    inline=True,
                )
                embedVar.add_field(
                    name="`channel`",
                    value="Returns the channel's profile from YouTube",
                    inline=True,
                )
                embedVar.add_field(
                    name="`playlist`",
                    value="Returns up to 5 youtube playlists based on the given YT channel",
                    inline=True,
                )
                embedVar.set_author(
                    name="Help - YouTube", icon_url=bot.user.display_avatar
                )
                await ctx.respond(embed=embedVar)
        except Exception as e:
            bot = self.bot
            embedVar = discord.Embed(title="Help", color=14414079)
            embedVar.description = "The query failed."
            embedVar.add_field(name="Error", value=e, inline=True)
            embedVar.set_thumbnail(url=bot.user.display_avatar)
            await ctx.respond(embed=embedVar)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


def setup(bot):
    bot.add_cog(rinhelp(bot))
