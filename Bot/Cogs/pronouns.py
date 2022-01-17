import discord
from discord.ext import commands
from discord.utils import get


# Disabled for now. needs more testing
class check_pronouns(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    @commands.is_owner()
    async def on_message(self, ctx):
        if ctx.author.id != self.bot.user.id and ctx.channel.name == "hanako-roles":
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
            msg = await ctx.channel.send(embed=embedVar)
            await msg.add_reaction("🧡")
            await msg.add_reaction(":heart:")
            await msg.add_reaction(":white_heart:")
            await msg.add_reaction(":green_heart:")
            await msg.add_reaction(":blue_heart:")
            await msg.add_reaction(":yellow_heart:")
            await msg.add_reaction(":purple_heart:")

            def check2(r, u):
                return u == ctx.author and str(r.emoji) in ":heart:"

            def check3(r, u):
                return u == ctx.author and str(r.emoji) in ":white_heart:"

            def check4(r, u):
                return u == ctx.author and str(r.emoji) in ":green_heart:"

            def check5(r, u):
                return u == ctx.author and str(r.emoji) in ":blue_heart:"

            def check6(r, u):
                return u == ctx.author and str(r.emoji) in ":yellow_heart:"

            def check7(r, u):
                return u == ctx.author and str(r.emoji) in ":purple_heart:"

            reaction, user = await self.bot.wait_for_reaction("reaction_add")
            if str(reaction.emoji) == "🧡":
                guild = ctx.guild
                await guild.create_role(name="He/Him", color=0xE67E22)
                member = ctx.message.author
                role = get(member.server.roles, name="He/Him")
                await bot.add_roles(member, "He/Him")
                await ctx.send("added roles")


def setup(bot):
    bot.add_cog(check_pronouns(bot))
