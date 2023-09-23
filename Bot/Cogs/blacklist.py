import discord
from discord import app_commands
from discord.ext import commands
from kumikocore import KumikoCore
from Libs.ui.blacklist import BlacklistPages
from Libs.utils import get_or_fetch_full_blacklist

HANGOUT_GUILD_ID = 1145897416160194590
TESTING_GUILD_ID = 970159505390325842
DONE_MSG = "Done."
NO_HANGOUT_BLOCK = "Can't block the hangout guild"
ID_DESC = "User or Guild ID to add"


class Blacklist(commands.Cog, command_attrs=dict(hidden=True)):
    """Blacklisting module for Kumiko"""

    def __init__(self, bot: KumikoCore) -> None:
        self.bot = bot
        self.pool = self.bot.pool

    @commands.guild_only()
    @commands.is_owner()
    @commands.hybrid_group(
        name="blacklist",
        fallback="view",
        hidden=True,
        guild_ids=[HANGOUT_GUILD_ID, TESTING_GUILD_ID],
    )
    async def blacklist(self, ctx: commands.Context) -> None:
        """Blacklist management module - No subcommands means viewing the blacklist"""
        cache = await get_or_fetch_full_blacklist(self.bot, self.pool)

        if cache is None:
            await ctx.send("No entries in the blacklist cache")
            return

        cache_to_list = [{k: v} for k, v in cache.items()]
        pages = BlacklistPages(entries=cache_to_list, ctx=ctx)
        await pages.start()

    @commands.guild_only()
    @commands.is_owner()
    @blacklist.command(name="add", hidden=True)
    @app_commands.guilds(HANGOUT_GUILD_ID, TESTING_GUILD_ID)
    @app_commands.describe(id=ID_DESC)
    async def add(self, ctx: commands.Context, id: str) -> None:
        """Blacklists the given user or guild ID"""
        obj = discord.Object(id=int(id))
        if obj.id != HANGOUT_GUILD_ID and obj.id != TESTING_GUILD_ID:
            query = """
            INSERT INTO blacklist (id, blacklist_status)
            VALUES ($1, $2) ON CONFLICT (id) DO NOTHING;
            """
            await self.pool.execute(query, obj.id, True)
            if obj.id not in self.bot.blacklist_cache:
                self.bot.add_to_blacklist_cache(obj.id)

            await ctx.send(DONE_MSG)
            return
        await ctx.send(NO_HANGOUT_BLOCK)

    @commands.guild_only()
    @commands.is_owner()
    @blacklist.command(name="delete", hidden=True)
    @app_commands.guilds(HANGOUT_GUILD_ID, TESTING_GUILD_ID)
    @app_commands.describe(id=ID_DESC)
    async def delete(self, ctx: commands.Context, id: str) -> None:
        """Un-blacklists the given user or guild ID"""
        obj = discord.Object(id=int(id))
        if obj.id != HANGOUT_GUILD_ID and obj.id != TESTING_GUILD_ID:
            query = """
            DELETE FROM blacklist
            WHERE id = $1;
            """
            await self.pool.execute(query, obj.id)
            if obj.id in self.bot.blacklist_cache:
                self.bot.remove_from_blacklist_cache(obj.id)

            await ctx.send(DONE_MSG)

            return

        await ctx.send(NO_HANGOUT_BLOCK)

    @commands.guild_only()
    @commands.is_owner()
    @blacklist.command(name="update", hidden=True)
    @app_commands.guilds(HANGOUT_GUILD_ID, TESTING_GUILD_ID)
    @app_commands.describe(id=ID_DESC, status="Status of the blacklist")
    async def update(self, ctx: commands.Context, id: str, status: bool) -> None:
        """Updates the blacklist entry for the given user or guild ID"""
        obj = discord.Object(id=int(id))
        if obj.id != HANGOUT_GUILD_ID and obj.id != TESTING_GUILD_ID:
            query = """
            UPDATE blacklist
            SET status = $2
            WHERE id = $1;
            """
            await self.pool.execute(query, obj.id, status)
            if id in self.bot.blacklist_cache:
                self.bot.update_blacklist_cache(obj.id, status)

            await ctx.send(DONE_MSG)
            return

        await ctx.send(NO_HANGOUT_BLOCK)


async def setup(bot: KumikoCore) -> None:
    await bot.add_cog(Blacklist(bot))
