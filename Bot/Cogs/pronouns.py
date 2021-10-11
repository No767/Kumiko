import discord
from discord.ext import commands


def check(reaction):
    return str(reaction.emoji) == ":orange_heart:"


class check_pronouns(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, ctx):
        if not ctx.author.id == self.bot.user.id and ctx.channel.name == "roles":
            bot = self.bot
            embedVar = discord.Embed(title="What are your pronouns?")
            embedVar.set_thumbnail(url=bot.user.avatar_url)
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
            reaction = await bot.wait_for("reaction_add", check=check)
            if reaction == ":orange_heart:" and ctx.author == self.bot.user:
                await ctx.channel.send("It is working")


def setup(bot):
    bot.add_cog(check_pronouns(bot))
