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
                embedVar = discord.Embed(title="Rin Help", color=14414079)
                embedVar.description = """
                        Welcome to Rin's Help Page! 
                        
                        Remember, the command prefix for this bot is `.`
                        In order to access the different categories, type the category name after the command. Here are the are the different categories that are available:
                        
                        - `admin`\n
                        - `twitter`\n
                        - `reddit`\n
                        - `minecraft`\n
                        - `fun`\n
                        - `instagram`\n
                        - `chat`\n
                        - `misc`\n
                        - `deviantart`\n
                        - `anime`\n
                        """
                embedVar.set_thumbnail(url=bot.user.avatar_url)
                await ctx.send(embed=embedVar)

            if str(search) == "admin":
                bot = self.bot
                name = bot.user.name
                id = bot.user.id
                embedVar = discord.Embed(
                    title="Rin Help - Admin", color=14414079)
                embedVar.description = """
                `botgrowth` - Tips based on bot statistics on how to reach more people!\n
                `prune` - Removes bot from servers smaller than the specified limit\n
                `botinfo` - Statistics about this bot\n
                `serverinfo` - Known server information\n
                `ping` - Checks the ping for the bot\n
                `ban` - Bans the specified user\n
                """
                embedVar.set_thumbnail(url=bot.user.avatar_url)
                await ctx.send(embed=embedVar)

            if str(search) == "twitter":
                bot = self.bot
                embedVar = discord.Embed(
                    title="Rin Help - Twitter", color=14414079)
                embedVar.description = """
                `rt` - Grabs Twitter user's timeline\n
                `rtupdatestatus` - Updates Twitter user's status\n
                `rtsearch` - Searches for twitter users\n
                
                **Note: Currently the Twitter Cog is broken. Reworking it soon**
                """
                embedVar.set_thumbnail(url=bot.user.avatar_url)
                await ctx.send(embed=embedVar)

            if str(search) == "reddit":
                bot = self.bot
                embedVar = discord.Embed(
                    title="Rin Help - Reddit", color=14414079)
                embedVar.description = """
                `reddit` - searches on reddit\n
                `transmeme` - searches on reddit that include trans and other LGBTQ+ subreddits\n
                `meme` - searches on reddit that include defined search topics regarding memes\n
                """
                embedVar.set_thumbnail(url=bot.user.avatar_url)
                await ctx.send(embed=embedVar)

            if str(search) == "minecraft":
                bot = self.bot
                embedVar = discord.Embed(title="Rin Help - MC", color=14414079)
                embedVar.description = """
                `javamcsrv` - Obtains Java server status\n
                `bedrockmcsrc` - Obtains Bedrock server status\n
                `hypixel` - Gain Insight in Hypixel's player data\n
                `hypixelcount` - Obtain the amount of players online within the servers\n
                `hypixelplayerstatus` - Determine if the player is online or not\n
                `skywarsinfo` - Get the position and score of the player within **ranked** skywars\n
                """
                embedVar.set_thumbnail(url=bot.user.avatar_url)
                await ctx.send(embed=embedVar)

            if str(search) == "fun":
                bot = self.bot
                embedVar = discord.Embed(
                    title="Rin Help - Fun", color=14414079)
                embedVar.description = """
                `pinger` - Annoys everyone with a message and allows for how much that message is sent for\n
                `valid` - Provides some valid feedback\n
                `mylvl` - Displays DisQuest Level\n
                `makeyourownbot` - Make your own discord bot with EasyBot framework by Chisaku-Dev\n
                `image` - Scraps Images on Deviantart\n
                `rank` - Displays the most active members of your server!\n
                `globalrank` - Displays the most active members of all servers that this bot is connected to!\n
                """
                embedVar.set_thumbnail(url=bot.user.avatar_url)
                await ctx.send(embed=embedVar)

            if str(search) == "instagram":
                bot = self.bot
                embedVar = discord.Embed(
                    title="Rin Help - Instagram", color=14414079)
                embedVar.description = """
                `iguserinfo` - Uses the User's Client ID in order to obtain Instagram User Info\n
                `igusersearch` - Searches for users on Instagram \n
                `igtaginfo` - Obtains Tag Info\n
                `igusernamecheck` - Checks if the specified username is taken or not
                
                **Note: Instagram likes to rate limit users like me with their private API. Make sure not to send too much requests, or else this cog will not work**
                """
                embedVar.set_thumbnail(url=bot.user.avatar_url)
                await ctx.send(embed=embedVar)

            if str(search) == "chat":
                bot = self.bot
                embedVar = discord.Embed(
                    title="Rin Help - Chat", color=14414079)
                embedVar.description = """
                `chathelp` - The chat is automatically generated based on prewritten responses. Responses that are not documented will be ignored\n
                `clear` - Clears number of messages specified from the channel in which the command was called\n
                """
                embedVar.set_thumbnail(url=bot.user.avatar_url)
                await ctx.send(embed=embedVar)

            if str(search) == "misc":
                bot = self.bot
                embedVar = discord.Embed(
                    title="Rin Help - Misc", color=14414079)
                embedVar.description = """
                `jisho` - Uses Jisho and JMDict in order to obtain info on a word in japanese\n
                `translate` - Translates the given message\n
                `rinhelp` - Rin's Help command\n
                """
                embedVar.set_thumbnail(url=bot.user.avatar_url)
                await ctx.send(embed=embedVar)

            if str(search) == "deviantart":
                bot = self.bot
                embedVar = discord.Embed(
                    title="Rin Help - Deviantart", color=14414079)
                embedVar.description = """
                `devartfind` - Finds art on DeviantArt via their public API\n
                `devartsearch` - Searches for art\n
                `devartuserget` - Obtains info on a user on DeviantArt\n
                """
                embedVar.set_thumbnail(url=bot.user.avatar_url)
                await ctx.send(embed=embedVar)
            if str(search) == "anime":
                bot = self.bot
                embedVar = discord.Embed(
                    title="Rin Help - Anime", color=14414079)
                embedVar.description = """
                `waifu` - Randomly selects a waifu from MyWaifuList\n
                `waifupics` - Searches for art from Waifiu.pics\n
                """
                embedVar.set_thumbnail(url=bot.user.avatar_url)
                await ctx.send(embed=embedVar)
        except:
            bot = self.bot
            embedVar = discord.Embed(title="Rin Help", color=14414079)
            embedVar.description = """The full list of commands can be found here: https://rin-docs.readthedocs.io/en/latest/rin-commands"""
            embedVar.set_thumbnail(url=bot.user.avatar_url)
            await ctx.send(embed=embedVar)


def setup(bot):
    bot.add_cog(rinhelp(bot))
