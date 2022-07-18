import re

import discord
from discord.commands import Option, SlashCommandGroup
from discord.ext import commands


class UserAvatar(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    avatar = SlashCommandGroup(
        "avatar", "Commands for the avatar command", guild_ids=[970159505390325842]
    )
    avatarGet = avatar.create_subgroup(
        "get", "Get the avatar of a user or bot", guild_ids=[970159505390325842]
    )

    @avatarGet.command(name="user")
    async def avatarGetUser(
        self, ctx, *, user: Option(str, "The username you wish to get")
    ):
        """Obtains the given user's avatar"""
        try:
            parsedUserID = int(re.sub("[^a-zA-Z0-9 ]", "", user))
            getUserInfo = await self.bot.fetch_user(parsedUserID)
            embed = discord.Embed()
            embed.title = f"{getUserInfo.name}#{getUserInfo.discriminator}"
            embed.set_image(url=getUserInfo.display_avatar.url)
            await ctx.respond(embed=embed)
        except Exception:
            await ctx.respond(
                embed=discord.Embed(
                    description="Oops, it looks like you may have not put in an actual discord username. Please try again."
                )
            )


def setup(bot):
    bot.add_cog(UserAvatar(bot))
