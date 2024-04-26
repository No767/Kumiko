from typing import Literal

import discord
from discord.ext import commands
from kumikocore import KumikoCore
from libs.ui.blacklist import BlacklistPages
from libs.utils.blacklist import BlacklistEntityType, get_blacklist

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

    def determine_type(self, type: Literal["user", "guild"]) -> BlacklistEntityType:
        if type == "user":
            return BlacklistEntityType.user
        return BlacklistEntityType.guild

    @commands.group(name="blacklist", invoke_without_command=True, hidden=True)
    @commands.is_owner()
    @commands.guild_only()
    async def blacklist(self, ctx: commands.Context) -> None:
        """Blacklist management module - No subcommands means viewing the blacklist"""
        query = """
        SELECT id, blacklist_status
        FROM blacklist;
        """
        records = await self.pool.fetch(query)
        if len(records) == 0:
            await ctx.send("No blacklist entries found")
            return

        cache_to_list = [
            {record["entity_id"]: record["blacklist_status"]} for record in records
        ]

        pages = BlacklistPages(entries=cache_to_list, ctx=ctx)
        await pages.start()

    @blacklist.command(name="add", hidden=True)
    async def add(
        self, ctx: commands.Context, id: discord.Object, type: Literal["user", "guild"]
    ) -> None:
        """Blacklists the given user or guild ID"""
        gid = id.id
        entity_type = self.determine_type(type)
        if not self.server_check(gid):
            query = """
            INSERT INTO blacklist (id, entity_id, entity_type)
            VALUES ($1, $2) ON CONFLICT (id) DO NOTHING;
            """
            await self.pool.execute(query, gid, entity_type)
            get_blacklist.cache_invalidate(gid, self.pool)
            await ctx.send(f"Done. Added ID {gid} (type: {type}) to the blacklist")
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
            get_blacklist.cache_invalidate(gid, self.pool)
            await ctx.send(f"Done. Removed ID {gid} from the blacklist")
            return

        await ctx.send(NO_HANGOUT_BLOCK)


async def setup(bot: KumikoCore) -> None:
    await bot.add_cog(Blacklist(bot))
