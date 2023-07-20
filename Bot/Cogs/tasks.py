import logging

from discord.ext import commands, tasks
from kumikocore import KumikoCore


class Tasks(commands.Cog, command_attrs=dict(hidden=True)):
    """Tasks that run in the background"""

    def __init__(self, bot: KumikoCore) -> None:
        self.bot = bot
        self.pool = self.bot.pool
        self.logger = logging.getLogger("discord")
        self.update_job_pay.start()

    async def cog_unload(self):
        self.update_job_pay.stop()

    @tasks.loop(hours=1)
    async def update_job_pay(self) -> None:
        """The internal task of updating jobs every hour

        The way it works is a three step process:

        1. Get all of the user's id within the database. It is guaranteed that all users in that table have an "account" already.
        2. Sum the pay amount of all of the jobs that the user is associated with
        3. Update the data

        The user of prepared statements make sense here since we are running these cursors through literally every single registered user. Which can get a lot
        """
        # is this inner join really needed?
        sumDataQuery = """
        SELECT SUM(job.pay_amount) AS total
        FROM job_lookup
        INNER JOIN job ON job.id = job_lookup.job_id
        WHERE job_lookup.worker_id = $1 AND job_lookup.listed = False
        GROUP BY job_lookup.worker_id;
        """
        updateQuery = """
        UPDATE eco_user
        SET petals = petals + $2
        WHERE id = $1;
        """
        async with self.pool.acquire() as conn:
            smt = await conn.prepare("SELECT id FROM eco_user")
            sumDataSmt = await conn.prepare(sumDataQuery)
            async with conn.transaction():
                async for record in smt.cursor():
                    id = dict(record)["id"]
                    total = await sumDataSmt.fetchval(id)
                    if total is not None:
                        await conn.execute(updateQuery, id, total)

    @update_job_pay.error
    async def on_update_pay_error(self, error) -> None:
        self.logger.exception(f"Error in update_pay: {error}")


async def setup(bot: KumikoCore) -> None:
    await bot.add_cog(Tasks(bot))
