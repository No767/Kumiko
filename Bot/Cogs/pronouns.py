import discord
from discord.ext import commands
from discord.utils import get


class check_pronouns(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, ctx):
        if ctx.author.id != self.bot.user.id and ctx.channel.name == "roles":
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
            reaction, user = await bot.wait_for(
                "reaction_add", check=lambda reaction, user: reaction.emoji == "🧡"
            )
            emoji = "🧡"
            if any(reaction.emoji == emoji for reaction in ctx.reactions):
                guild = ctx.guild
                await guild.create_role(name="He/Him", color=0xE67E22)
                member = ctx.message.author
                role = get(member.server.roles, name="He/Him")
                await bot.add_roles(member, role)


def setup(bot):
    bot.add_cog(check_pronouns(bot))
