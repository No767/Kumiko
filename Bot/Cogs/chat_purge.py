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
        text_channels = guild.text_channels
        voice_channels = guild.voice_channels
        members = guild.member_count
        premium_members = guild.premium_subscription_count
        max_members = guild.max_members
        location = guild.region
        epox = guild.created_at
        owner = guild.owner_id
        explicit = guild.explicit_content_filter
        emojis = guild.emojis
        embed = discord.Embed(color=plugin_tools.discord_colors())
        embed.title = "Server Info"
        embed.add_field(name="Name", value=name, inline=True)
        embed.add_field(name="# of channels", value=len(channels), inline=True)
        embed.add_field(
            name="# of text channels", value=len(text_channels), inline=True
        )
        embed.add_field(
            name="# of voice channels", value=len(voice_channels), inline=True
        )
        embed.add_field(
            name="# of nitro boosted members", value=premium_members, inline=True
        )
        embed.add_field(
            name="# of members", value=f"{members}/{max_members}", inline=True
        )
        embed.add_field(name="Located in", value=location, inline=True)
        embed.add_field(name="Created on", value=epox, inline=True)
        embed.add_field(
            name="Explicit content filter enabled for", value=explicit, inline=True
        )
        embed.add_field(name="List of all emojis", value=emojis, inline=True)
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
