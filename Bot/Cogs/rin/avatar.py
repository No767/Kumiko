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
        self, ctx, *, user: Option(discord.Member, "The username you wish to get")
    ):
        """Obtains the given user's avatar"""
        try:
            embed = discord.Embed()
            embed.title = f"{user.display_name}#{user.discriminator}'s avatar"
            embed.set_image(url=user.display_avatar.url)
            await ctx.respond(embed=embed)
        except Exception as e:
            await ctx.respond(
                embed=discord.Embed(
                    title="Oops, an error occurred!",
                    description=f"{type(e).__name__}: {str(e)}",
                )
            )


def setup(bot):
    bot.add_cog(UserAvatar(bot))
