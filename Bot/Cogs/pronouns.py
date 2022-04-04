import discord
from discord.ext import commands


# Disabled for now. needs more testing
class check_pronouns(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    @commands.is_owner()
    async def on_message(self, ctx):
        self.bot
        embedVar = discord.Embed(title="What are your pronouns?")
        embedVar.description = """
            :orange_heart: - he/him
            :heart: - she/her
            :white_heart: - they/them
            :green_heart: - he/they
            :blue_heart: - she/they
            :yellow_heart: - he/she/they
            :purple_heart: - ask
            """
        embedVar.set_footer(
            text="React to those emojis to get a role assigned with those pronouns!"
        )
        await ctx.channel.send(embed=embedVar)


def setup(bot):
    bot.add_cog(check_pronouns(bot))
