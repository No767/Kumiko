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
                        
                        - `admin`
                        - `twitter`
                        - `reddit`
                        - `mc`
                        - `fun`
                        - `instagram`
                        - `chat`
                        - `misc`
                        - `deviantart`
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
                `botgrowth` - Tips based on bot statistics on how to reach more people!
                `prune` - Removes bot from servers smaller than the specified limit
                `botinfo` - Statistics about this bot
                `serverinfo` - Known server information
                `rinping` - Checks the ping for the bot
                `ban` - Bans the specified user
                """
                embedVar.set_thumbnail(url=bot.user.avatar_url)
                await ctx.send(embed=embedVar)

            if str(search) == "twitter":
                bot = self.bot
                embedVar = discord.Embed(
                    title="Rin Help - Twitter", color=14414079)
                embedVar.description = """
                `rt` - Grabs Twitter user's timeline
                `rtupdatestatus` - Updates Twitter user's status
                `rtsearch` - Searches for twitter users
                
                **Note: Currently the Twitter Cog is broken. Reworking it soon**
                """
                embedVar.set_thumbnail(url=bot.user.avatar_url)
                await ctx.send(embed=embedVar)

            if str(search) == "reddit":
                bot = self.bot
                embedVar = discord.Embed(
                    title="Rin Help - Reddit", color=14414079)
                embedVar.description = """
                `reddit` - searches on reddit
                `transmeme` - searches on reddit that include trans and other LGBTQ+ subreddits
                `meme` - searches on reddit that include defined search topics regarding memes
                """
                embedVar.set_thumbnail(url=bot.user.avatar_url)
                await ctx.send(embed=embedVar)

            if str(search) == "mc":
                bot = self.bot
                embedVar = discord.Embed(title="Rin Help - MC", color=14414079)
                embedVar.description = """
                `javamcsrv` - Obtains Java server status
                `bedrockmcsrc` - Obtains Bedrock server status
                """
                embedVar.set_thumbnail(url=bot.user.avatar_url)
                await ctx.send(embed=embedVar)

            if str(search) == "fun":
                bot = self.bot
                embedVar = discord.Embed(
                    title="Rin Help - Fun", color=14414079)
                embedVar.description = """
                `pinger` - Annoys everyone with a message and allows for how much that message is sent for
                `valid` - Provides some valid feedback
                `waifu` - Randomly selects a waifu
                `mylvl` - Displays DisQuest Level
                `makeyourownbot` - Make your own discord bot with EasyBot framework by Chisaku-Dev
                `image` - Scraps Images on Deviantart
                `rank` - Displays the most active members of your server!
                `globalrank` - Displays the most active members of all servers that this bot is connected to!
                """
                embedVar.set_thumbnail(url=bot.user.avatar_url)
                await ctx.send(embed=embedVar)

            if str(search) == "instagram":
                bot = self.bot
                embedVar = discord.Embed(
                    title="Rin Help - Instagram", color=14414079)
                embedVar.description = """
                `iguserinfo` - Uses the User's Client ID in order to obtain Instagram User Info
                `igusersearch` - Searches for users on Instagram 
                `igtaginfo` - Obtains Tag Info
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
                `chathelp` - The chat is automatically generated based on prewritten responses. Responses that are not documented will be ignored
                `clear` - Clears number of messages specified from the channel in which the command was called
                """
                embedVar.set_thumbnail(url=bot.user.avatar_url)
                await ctx.send(embed=embedVar)

            if str(search) == "misc":
                bot = self.bot
                embedVar = discord.Embed(
                    title="Rin Help - Misc", color=14414079)
                embedVar.description = """
                `jisho` - Uses Jisho and JMDict in order to obtain info on a word in japanese
                `translate` - Translates the given message
                `rinhelp` - Rin's Help command
                """
                embedVar.set_thumbnail(url=bot.user.avatar_url)
                await ctx.send(embed=embedVar)

            if str(search) == "deviantart":
                bot = self.bot
                embedVar = discord.Embed(
                    title="Rin Help - Deviantart", color=14414079)
                embedVar.description = """
                `devartfind` - Finds art on DeviantArt via their public API
                `devartsearch` - Searches for art
                `devartuserget` - Obtains info on a user on DeviantArt
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
