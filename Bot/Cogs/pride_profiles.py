import discord
from discord import app_commands
from discord.ext import commands
from kumikocore import KumikoCore
from Libs.cog_utils.pride_profiles import present_info
from Libs.ui.pride_profiles import (
    ConfigureView,
    ConfirmRegisterView,
    DeleteProfileView,
    PrideProfileSearchPages,
    PrideProfileStatsPages,
)
from Libs.utils import ConfirmEmbed, Embed


class PrideProfiles(commands.Cog, name="Pride Profiles"):
    """Create pride profiles to let others know who you are!

    Again, this is meant to be used seriously as a resource for the LGTBQ+ community
    """

    def __init__(self, bot: KumikoCore) -> None:
        self.bot = bot
        self.pool = self.bot.pool

    @property
    def display_emoji(self) -> discord.PartialEmoji:
        return discord.PartialEmoji.from_str("<:BlahajPrideHeart:1096898214214516866>")

    @commands.hybrid_group(name="pride-profiles", fallback="info")
    @app_commands.describe(user="The user to look for")
    async def pride_profiles(
        self, ctx: commands.Context, user: discord.User = commands.Author
    ) -> None:
        """Look at a pride profile"""
        ...
        query = """
        SELECT * FROM pride_profiles
        WHERE id = $1;
        """
        update_views_count = """
        UPDATE pride_profiles
        SET views = views + 1
        WHERE id = $1;
        """
        async with self.pool.acquire() as conn:
            rows = await conn.fetchrow(query, user.id)
            if rows is None:
                await ctx.send(
                    f"You or the user has no profile. Run `{ctx.prefix}pride-profiles register` in order to do so"
                )
                return

            await conn.execute(update_views_count, user.id)
            records = dict(rows)
            embed = Embed(title=f"{user.global_name}'s Profile")
            embed.description = present_info(records, records["id"])
            embed.set_thumbnail(url=user.display_avatar.url)
            await ctx.send(embed=embed)

    @pride_profiles.command(name="register")
    async def register(self, ctx: commands.Context) -> None:
        """Register a pride profile"""
        view = ConfirmRegisterView(ctx.author.id, self.pool)
        embed = ConfirmEmbed()
        embed.description = "Are you sure you want to register for a pride profile? It's very exciting and fun"
        await ctx.send(embed=embed, view=view, ephemeral=True)

    @pride_profiles.command(name="configure", aliases=["config"])
    async def configure(self, ctx: commands.Context) -> None:
        """Configure your pride profile"""
        view = ConfigureView(self.pool)
        embed = Embed(title="Configuring your pride profile")
        embed.description = "In order to configure your pride profile, select at one of the categories listed in the drop down."
        await ctx.send(embed=embed, view=view, ephemeral=True)

    @pride_profiles.command(name="top")
    async def top(self, ctx: commands.Context) -> None:
        """Gets the top 100 most viewed profiles globally"""
        query = """
        SELECT id, name, views
        FROM pride_profiles
        ORDER BY views DESC
        LIMIT 100;
        """
        rows = await self.pool.fetch(query)
        if rows:
            pages = PrideProfileStatsPages(entries=rows, ctx=ctx, per_page=10)
            await pages.start()
        else:
            await ctx.send("No names were found.")

    @pride_profiles.command(name="search")
    @app_commands.describe(name="The preferred name to search")
    async def search(self, ctx: commands.Context, name: str) -> None:
        """Searches for a profile using the given name"""

        query = """
        SELECT id, name, pronouns
        FROM pride_profiles
        WHERE name % $1
        ORDER BY similarity(name, $1) DESC
        LIMIT 100;
        """
        rows = await self.pool.fetch(query, name)
        if rows:
            pages = PrideProfileSearchPages(entries=rows, ctx=ctx, per_page=10)
            await pages.start()
        else:
            await ctx.send("No names were found.")

    @pride_profiles.command(name="delete")
    async def delete(self, ctx: commands.Context) -> None:
        """Permanently deletes your pride profile"""
        view = DeleteProfileView(ctx.author.id, self.pool)
        embed = ConfirmEmbed()
        embed.description = "Are you sure you really want to delete your profile?"
        await ctx.send(embed=embed, view=view, ephemeral=True)


async def setup(bot: KumikoCore) -> None:
    await bot.add_cog(PrideProfiles(bot))
