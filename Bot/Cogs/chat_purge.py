import discord
from Cogs import plugin_tools
from discord.ext import commands


class Utility(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="serverinfo", help="Known server information")
    async def serverinfo(self, ctx):
        guild = ctx.guild
        name = guild.name
        channels = guild.channels
        members = guild.member_count
        premium_members = guild.premium_subscription_count
        max_members = guild.max_members
        location = guild.region
        epox = guild.created_at
        owner = guild.owner_id
        explicit = guild.explicit_content_filter
        embed = discord.Embed(color=plugin_tools.discord_colors())
        embed.title = "Server Info"
        embed.description = f"""
        Name: {name}\n
        # of channels: {len(channels)}\n
        # of nitro boosted members: {premium_members}\n
        # of members: {members}/{max_members}\n
        Located in {location}\n
        Created on {epox}\n
        Owned by UID: {owner}\n
        Explicit content filter enabled for {explicit}\n
        """
        embed.set_thumbnail(url=guild.icon_url)
        await ctx.send(embed=embed)

    @commands.command(
        name="clear",
        help="Clears number of messages specified from the channel in which the command was called",
    )
    async def clear(self, ctx, number_of_messages: int):
        await ctx.channel.purge(limit=number_of_messages + 1)
        await ctx.send(
            embed=plugin_tools.fast_embed(
                f"{number_of_messages} messages were deleted"
            ),
            delete_after=3,
        )


def setup(bot):
    bot.add_cog(Utility(bot))
