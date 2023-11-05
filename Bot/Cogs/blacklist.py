import discord
from discord.ext import commands
from kumikocore import KumikoCore
from Libs.ui.blacklist import BlacklistPages
from Libs.utils import get_or_fetch_full_blacklist

DONE_MSG = "Done."
NO_HANGOUT_BLOCK = "Can't block these servers"


class Blacklist(commands.Cog, command_attrs=dict(hidden=True)):
    """Blacklisting module for Kumiko"""

    def __init__(self, bot: KumikoCore) -> None:
        self.bot = bot
        self.pool = self.bot.pool

    def server_check(self, id: int):
        servers = {
            1145897416160194590,  # Noelle's Hangout
            970159505390325842,  # Kumiko Testing Server,
            454357482102587393,  # Noelle
        }
        return id in servers

    @commands.group(name="blacklist", invoke_without_command=True, hidden=True)
    @commands.is_owner()
    @commands.guild_only()
    async def blacklist(self, ctx: commands.Context) -> None:
        """Blacklist management module - No subcommands means viewing the blacklist"""
        cache = await get_or_fetch_full_blacklist(self.bot, self.pool)

        if cache is None:
            await ctx.send("No entries in the blacklist cache")
            return

        cache_to_list = [{k: v} for k, v in cache.items()]
        pages = BlacklistPages(entries=cache_to_list, ctx=ctx)
        await pages.start()

    @blacklist.command(name="add", hidden=True)
    async def add(self, ctx: commands.Context, id: discord.Object) -> None:
        """Blacklists the given user or guild ID"""
        gid = id.id
        if not self.server_check(gid):
            query = """
            INSERT INTO blacklist (id, blacklist_status)
            VALUES ($1, $2) ON CONFLICT (id) DO NOTHING;
            """
            await self.pool.execute(query, gid, True)
            if gid not in self.bot.blacklist_cache:
                self.bot.add_to_blacklist_cache(gid)

            await ctx.send(DONE_MSG)
            return
        await ctx.send(NO_HANGOUT_BLOCK)

    @blacklist.command(name="delete", hidden=True)
    async def delete(self, ctx: commands.Context, id: discord.Object) -> None:
        """Un-blacklists the given user or guild ID"""
        gid = id.id

        if not self.server_check(gid):
            query = """
            DELETE FROM blacklist
            WHERE id = $1;
            """
            await self.pool.execute(query, gid)
            if gid in self.bot.blacklist_cache:
                self.bot.remove_from_blacklist_cache(gid)

            await ctx.send(DONE_MSG)

            return

        await ctx.send(NO_HANGOUT_BLOCK)


async def setup(bot: KumikoCore) -> None:
    await bot.add_cog(Blacklist(bot))
