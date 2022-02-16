import asyncio

import discord
import discord.ext
import uvloop
from discord.commands import Option, slash_command
from discord.ext import commands


class kumikoHelp(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.last_member = None

    @slash_command(
        name="kumikohelp",
        description="The Help Page for Kumiko",
        guild_ids=[866199405090308116],
    )
    async def kumikoHelp(
        self,
        ctx,
        *,
        category: Option(
            str,
            choices=[
                "Twitter",
                "Reddit",
                "Minecraft",
                "Hypixel",
                "Fun",
                "Misc",
                "Instagram",
                "DeviantArt",
                "Anime",
                "Top.gg",
                "Pinterest",
                "MyAnimeList/Jikan",
                "YouTube",
                "Tenor",
                "OpenAI",
            ],
            required=False,
        )
    ):
        try:
            if category is None:
                bot = self.bot
                embedVar = discord.Embed(color=14414079)
                embedVar.description = """
                        **[GitHub](https://github.com/No767/Kumiko)** | **[Issue Tracker](https://github.com/No767/Kumiko/issues)** 
                        """
                embedVar.add_field(
                    name="Twitter", value="`/kumikohelp twitter`", inline=True
                )
                embedVar.add_field(
                    name="Twitter", value="`/kumikohelp twitter`", inline=True
                )
                embedVar.add_field(
                    name="Minecraft", value="`/kumikohelp mc`", inline=True)
                embedVar.add_field(
                    name="Hypixel", value="`/kumikohelp hypixel`", inline=True
                )
                embedVar.add_field(
                    name="Fun", value="`/kumikohelp fun`", inline=True)
                embedVar.add_field(
                    name="Instagram", value="`/kumikohelp ig`", inline=True)
                embedVar.add_field(
                    name="Misc", value="`/kumikohelp misc`", inline=True)
                embedVar.add_field(
                    name="Deviantart", value="`/kumikohelp da`", inline=True
                )
                embedVar.add_field(
                    name="Minecraft", value="`/kumikohelp mc`", inline=True
                )
                embedVar.add_field(
                    name="Fun", value="`/kumikohelp fun`", inline=True)
                embedVar.add_field(
                    name="Instagram", value="`/kumikohelp ig`", inline=True
                )
                embedVar.add_field(
                    name="Chat", value="`/kumikohelp chat`", inline=True)
                embedVar.add_field(
                    name="Misc", value="`/kumikohelp misc`", inline=True)
                embedVar.add_field(
                    name="Deviantart", value="`/kumikohelp da`", inline=True
                )
                embedVar.add_field(
                    name="Anime", value="`/kumikohelp anime`", inline=True
                )
                embedVar.add_field(
                    name="Top.gg", value="`/kumikohelp topgg`", inline=True
                )
                embedVar.add_field(
                    name="Pinterest", value="`/kumikohelp pinterest`", inline=True
                )
                embedVar.add_field(
                    name="MyAnimeList/Jikan", value="`/kumikohelp jikan`", inline=True
                )
                embedVar.add_field(
                    name="YouTube", value="`/kumikohelp youtube`", inline=True
                )
                embedVar.add_field(
                    name="Tenor", value="`/kumikohelp tenor`", inline=True
                )
                embedVar.add_field(
                    name="OpenAI", value="`/kumikohelp openai`", inline=True
                )
                embedVar.set_author(
                    name="Kumiko Help", icon_url=bot.user.display_avatar
                )
                embedVar.set_footer(
                    text='Remember, the command prefix for this bot is "/"'
                )
                await ctx.respond(embed=embedVar)

            if category in ["twitter", "Twitter"]:
                bot = self.bot
                embedVar = discord.Embed(color=14414079)
                embedVar.add_field(
                    name="`twitter-search`",
                    value="Grabs 5 most recent tweets from the specified user",
                    inline=True,
                )
                embedVar.add_field(
                    name="`twitter-user`",
                    value="Grabs info about the specified user",
                    inline=True,
                )
                embedVar.set_author(
                    name="Kumiko Help - Twitter", icon_url=bot.user.display_avatar
                )
                await ctx.respond(embed=embedVar)

            if category in ["reddit", "Reddit"]:
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
                    name="Kumiko Help - Reddit", icon_url=bot.user.display_avatar
                )
                await ctx.respond(embed=embedVar)

            if category in ["minecraft", "mc", "Minecraft"]:
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
                    name="`java`", value="Alias for `javamcsrv`", inline=True
                )
                embedVar.add_field(
                    name="`bedrock`", value="Alias for `bedrockmcsrv", inline=True
                )
                embedVar.add_field(
                    name="`spiget-search`",
                    value="Searches for Minecraft plugins via Spiget and returns information on such plugin",
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
                    name="Kumiko Help - Minecraft", icon_url=bot.user.display_avatar
                )
                await ctx.respond(embed=embedVar)
            if category in ["Hypixel", "hypixel"]:
                bot = self.bot
                embedVar = discord.Embed(color=14414079)
                embedVar.add_field(
                    name="`hypixel-user`",
                    value="Gain Insight in Hypixel's player data",
                    inline=True,
                )
                embedVar.add_field(
                    name="`hypixel-count`",
                    value="Obtain the amount of players online within the servers",
                    inline=True,
                )
                embedVar.add_field(
                    name="`hypixel-player-status`",
                    value="Determine if the player is online or not",
                    inline=True,
                )
                embedVar.add_field(
                    name="`hypixel-punishments-stats`",
                    value="Returns some stats about the amount of punishments given on Hypixel",
                    inline=True,
                )
                embedVar.set_author(
                    name="Rin Help - Hypixel", icon_url=bot.user.display_avatar
                )
                await ctx.respond(embed=embedVar)

            if category in ["fun", "Fun"]:
                bot = self.bot
                embedVar = discord.Embed(color=14414079)
                embedVar.add_field(
                    name="`mylvl`", value="Displays DisQuest Level", inline=True
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
                embedVar.set_author(
                    name="Kumiko Help - Fun", icon_url=bot.user.display_avatar
                )
                await ctx.respond(embed=embedVar)

            if category in ["instagram", "ig", "Instgram"]:
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
                    text="Note: There is a 20 sec cooldown for each command. This is to prevent rate limiting."
                )
                embedVar.set_author(
                    name="Kumiko Help - Instagram", icon_url=bot.user.display_avatar
                )
                await ctx.respond(embed=embedVar)

            if category in ["misc", "Misc"]:
                bot = self.bot
                embedVar = discord.Embed(color=14414079)
                embedVar.add_field(
                    name="`jisho`",
                    value="Uses Jisho and JMDict in order to obtain info on a word in Japanese",
                    inline=True,
                )
                embedVar.add_field(
                    name="`translate`",
                    value="Translates the given message to any language supported by Google Translate",
                    inline=True,
                )
                embedVar.add_field(
                    name="`kumikohelp`", value="Kumiko's Help command", inline=True
                )
                embedVar.add_field(
                    name="`kumikoinvite`",
                    value="Kumiko's invite links. Also can be reached with `.invite`.",
                    inline=True,
                )
                embedVar.add_field(
                    name="`version`",
                    value="Checks for current version of Rin",
                    inline=True,
                )
                embedVar.add_field(
                    name="`uptime`", value="Checks for Kumiko's Uptime", inline=True
                )
                embedVar.add_field(
                    name="`botinfo`", value="Statistics about this bot", inline=True
                )
                embedVar.add_field(
                    name="`ping`", value="Checks the ping for the bot", inline=True
                )
                embedVar.set_author(
                    name="Kumiko Help - Misc", icon_url=bot.user.display_avatar
                )
                await ctx.respond(embed=embedVar)

            if category in ["deviantart", "da", "DevintArt"]:
                bot = self.bot
                embedVar = discord.Embed(color=14414079)
                embedVar.add_field(
                    name="`deviantart-item`",
                    value="Returns image and some info about that item",
                    inline=True,
                )
                embedVar.add_field(
                    name="`deviantart-newest`",
                    value="Returns 5 newest art based on selected category",
                    inline=True,
                )
                embedVar.add_field(
                    name="`deviantart-popular`",
                    value="Returns 5 popular works of art based on selected category",
                    inline=True,
                )
                embedVar.add_field(
                    name="`deviantart-tag-search`",
                    value="Returns 5 works of art based on selected tags",
                    inline=True,
                )
                embedVar.add_field(
                    name="`deviantart-user`",
                    value="Returns info about the given user",
                    inline=True,
                )
                embedVar.set_footer(
                    text='These cmds have the prefix of "deviantart". This prefix can be swapped out for "da" instead. For example, the "deviantart-item" cmd can be shorten to "da-item"'
                )
                embedVar.set_author(
                    name="Kumiko Help - Deviantart", icon_url=bot.user.display_avatar
                )
                await ctx.respond(embed=embedVar)

            if category in ["anime", "Anime"]:
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
                embedVar.set_author(
                    name="Kumiko Help - Anime", icon_url=bot.user.display_avatar
                )
                await ctx.respond(embed=embedVar)

            if category in [
                "jikan",
                "jk",
                "myanimelist",
                "mal",
                "MyAnimeList/Jikan",
            ]:
                bot = self.bot
                embedVar = discord.Embed(color=14414079)
                embedVar.add_field(
                    name="`jikan-anime`",
                    value="Seaches on Jikan/MyAnimeList and provides info about the given anime",
                    inline=True,
                )
                embedVar.add_field(
                    name="`jikan-manga`",
                    value="Seaches on Jikan/MyAnimeList and provides info about the given manga",
                    inline=True,
                )
                embedVar.add_field(
                    name="`jikan-top`",
                    value="Returns the Top 10 items on Jikan/MAL",
                    inline=True,
                )
                embedVar.add_field(
                    name="`jikan-season`",
                    value="Returns 5 animes within those given years and seasons",
                    inline=True,
                )
                embedVar.add_field(
                    name="`jikan-season-later`",
                    value="Returns 5 animes that are already planned for viewing in the future",
                    inline=True,
                )
                embedVar.set_footer(
                    text='Also note that the prefix can be shorten down to "jk"'
                )
                embedVar.set_author(
                    name="Kumiko Help - MyAnimeList/Jikan",
                    icon_url=bot.user.display_avatar,
                )
                await ctx.respond(embed=embedVar)

            if category in ["topgg", "Top.gg"]:
                bot = self.bot
                embedVar = discord.Embed(color=14414079)
                embedVar.add_field(
                    name="`topgg-search`",
                    value="Returns details about 1 bot searched on Top.gg",
                    inline=True,
                )
                embedVar.add_field(
                    name="`topgg-search-user`",
                    value="Returns info about user on Top.gg",
                    inline=True,
                )
                embedVar.set_author(
                    name="Kumiko Help - Topgg", icon_url=bot.user.display_avatar
                )
                await ctx.respond(embed=embedVar)

            if category in ["pinterest", "pt", "Pinterest"]:
                bot = self.bot
                embedVar = discord.Embed(color=14414079)
                embedVar.add_field(
                    name="`pinterest-user`",
                    value="Grabs info about the user that is logged in",
                    inline=True,
                )
                embedVar.add_field(
                    name="`pinterest-pins`",
                    value="Grabs Pins from the user that is logged in",
                    inline=True,
                )
                embedVar.add_field(
                    name="`pinterest-board`", value="Info about the board", inline=True
                )
                embedVar.set_footer(
                    text='The Pinterest cmds also have aliases just like Jikan and DeviantArt. The alias prefix is "pt". Note that the Pinterest API only supports getting info about the user that it is logged into, which means it is grabbing info from my own account. It is not recommended to use this service.'
                )
                embedVar.set_author(
                    name="Kumiko Help - Pinterest", icon_url=bot.user.display_avatar
                )
                await ctx.respond(embed=embedVar)

            if category in ["youtube", "yt", "YouTube"]:
                bot = self.bot
                embedVar = discord.Embed(color=14414079)
                embedVar.add_field(
                    name="`youtube-search`",
                    value="Returns 5 videos given the search query",
                    inline=True,
                )
                embedVar.add_field(
                    name="`youtube-channel`",
                    value="Returns info about the given channel",
                    inline=True,
                )
                embedVar.add_field(
                    name="`youtube-playlists`",
                    value="Finds and returns 5 playlists from the given channel",
                    inline=True,
                )
                embedVar.add_field(
                    name="`youtube-comments`",
                    value="Returns 5 comments (sorted by time) from the given video",
                    inline=True,
                )
                embedVar.add_field(
                    name="`youtube-video`",
                    value="Return info about the given video",
                    inline=True,
                )
                embedVar.set_footer(
                    text='Note that the alias prefix is "yt". This means that for example, the cmd "youtube-search" can be shorten down to "yt-search"'
                )
                embedVar.set_author(
                    name="Kumiko Help - YouTube", icon_url=bot.user.display_avatar
                )
                await ctx.respond(embed=embedVar)

            if category in ["tenor", "Tenor"]:
                bot = self.bot
                embedVar = discord.Embed(color=14414079)
                embedVar.add_field(
                    name="`tenor-search-multiple`",
                    value="Searches 5 gifs from Tenor",
                    inline=True,
                )
                embedVar.add_field(
                    name="`tenor-search-one`",
                    value="Searches for 1 gif on Tenor",
                    inline=True,
                )
                embedVar.add_field(
                    name="`tenor-trending`",
                    value="Gets 5 trending gifs from Tenor",
                    inline=True,
                )
                embedVar.add_field(
                    name="`tenor-search-suggestions`",
                    value="Provies some search suggetsions from Tenor",
                    inline=True,
                )
                embedVar.add_field(
                    name="`tenor-trending-terms`",
                    value="Returns some trending terms",
                    inline=True,
                )
                embedVar.add_field(
                    name="`tenor-gif`", value="SEarches for 1 gif on Tenor", inline=True
                )
                embedVar.add_field(
                    name="`tenor-random`",
                    value="Returns a random gif based on the search term",
                    inline=True,
                )
                embedVar.set_author(
                    name="Kumiko Help - Tenor", icon_url=bot.user.display_avatar
                )
                await ctx.respond(embed=embedVar)

            if category in ["openai", "ai", "gpt-3", "OpenAI"]:
                bot = self.bot
                embedVar = discord.Embed(color=14414079)
                embedVar.add_field(
                    name="`openai-complete`",
                    value="Completes a sentence using GPT-3",
                    inline=True,
                )
                embedVar.add_field(
                    name="`openai-classify`",
                    value="Classifies a sentence into negative or positive (using AI)",
                    inline=True,
                )
                embedVar.add_field(
                    name="`openai-answers`",
                    value="Generates answers written by AI for a given question",
                    inline=True,
                )
                embedVar.set_author(
                    name="Kumiko Help - OpenAI", icon_url=bot.user.display_avatar
                )
                await ctx.respond(embed=embedVar)

        except Exception as e:
            bot = self.bot
            embedVar = discord.Embed(title="Rin Help", color=14414079)
            embedVar.description = "The query failed."
            embedVar.add_field(name="Error", value=e, inline=True)
            embedVar.set_thumbnail(url=bot.user.display_avatar)
            await ctx.respond(embed=embedVar)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


def setup(bot):
    bot.add_cog(kumikoHelp(bot))
