import discord
from discord.ext import commands


class mute_user(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="mute")
    @commands.has_permissions(manage_messages=True)
    async def on_message(self, ctx, *, member: discord.Member, reason=None):
        guild = ctx.guild
        mutedRole = discord.utils.get(guild.roles, name="Time Out Corner")
        if not mutedRole:
            mutedRole = await guild.create_role(name="Time Out Corner")
            for channel in guild.channels:
                await channel.set_permissions(
                    mutedRole,
                    speak=False,
                    send_messages=False,
                    read_message_history=True,
                    read_messages=False,
                )
        embedVar = discord.Embed()
        embedVar.description = f"{member.mention} was muted for {reason}"
        await ctx.send(embed=embedVar)
        await member.add_roles(mutedRole, reason=reason)
        await member.send(f"You have been muted for {reason}")


class unmute_user(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="unmute")
    @commands.has_permissions(manage_messages=True)
    async def on_message(ctx, member: discord.Member):
        mutedRole = discord.utils.get(ctx.guild.roles, name="Time Out Corner")
        await member.remove_roles(mutedRole)
        await member.send("You have unmuted")
        embedVar = discord.Embed()
        embedVar.description = "Unmuted {member.mention}"
        await ctx.send(embed=embedVar)


def setup(bot):
    bot.add_cog(mute_user(bot))
    bot.add_cog(unmute_user(bot))
