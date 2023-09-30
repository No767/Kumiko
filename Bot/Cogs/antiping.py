from discord import PartialEmoji
from discord.ext import commands
from kumikocore import KumikoCore
from Libs.cog_utils.antiping import AntiPingSession

NO_AP_SESSION = "You do not have an antiping session active"


class AntiPing(commands.Cog, name="Anti-Ping"):
    """Configure antiping settings"""

    def __init__(self, bot: KumikoCore):
        self.bot = bot
        self.pool = self.bot.pool

    @property
    def display_emoji(self) -> PartialEmoji:
        return PartialEmoji.from_str("<:thinkPing2:542441704704180234>")

    @commands.hybrid_group(name="antiping", aliases=["ap"])
    async def antiping(self, ctx: commands.Context) -> None:
        """Commands to manage the anti-ping module"""
        if ctx.invoked_subcommand is None:
            await ctx.send_help(ctx.command)

    # TODO: Add an optional dt for scheduling purposes
    @antiping.command(name="start")
    async def start(self, ctx: commands.Context) -> None:
        """Starts an antiping session"""
        if ctx.author.id in self.bot.antiping_cache:
            await ctx.send("You're already on the antiping list!")
            return

        create_session = """
        INSERT INTO antiping_sessions (user_id, session_enabled)
        VALUES ($1, True) ON CONFLICT (user_id) DO 
        UPDATE SET session_enabled = True;
        """
        get_active_session = """
        SELECT id FROM antiping_sessions WHERE user_id = $1 AND session_enabled = True;
        """

        async with self.pool.acquire() as conn:
            await conn.execute(create_session, ctx.author.id)
            session_id = await conn.fetchval(get_active_session, ctx.author.id)
            self.bot.antiping_cache[ctx.author.id] = AntiPingSession(
                session_id=session_id, enabled=True
            )
            await ctx.send(
                f"Global Antiping session started for {ctx.author.global_name}"
            )

    @antiping.command(name="stop")
    async def stop(self, ctx: commands.Context) -> None:
        """Stops an active antiping session"""
        if ctx.author.id not in self.bot.antiping_cache:
            await ctx.send(NO_AP_SESSION)
            return

        # One user can only have one active session at a time
        get_active_session = """
        SELECT id FROM antiping_sessions WHERE user_id = $1 AND session_enabled = True;
        """
        remove_session = """
        DELETE FROM antiping_sessions WHERE id = $1 AND user_id = $2;
        """
        async with self.pool.acquire() as conn:
            active_session_id = await conn.fetchval(get_active_session, ctx.author.id)
            if active_session_id is None:
                # Should not fire but just in case
                await ctx.send(NO_AP_SESSION)
                return

            await conn.execute(remove_session, active_session_id, ctx.author.id)
            self.bot.antiping_cache.pop(ctx.author.id)
            await ctx.send(f"Antiping session stopped for {ctx.author.global_name}")

    @antiping.command(name="status")
    async def status(self, ctx: commands.Context) -> None:
        """Obtains info of the current active antiping session"""
        current_session = self.bot.antiping_cache.get(ctx.author.id)
        if current_session is None:
            await ctx.send(NO_AP_SESSION)
            return

        # TODO - Revamp this
        await ctx.send(f"Current antiping session status: {current_session}")


async def setup(bot: KumikoCore) -> None:
    await bot.add_cog(AntiPing(bot))
