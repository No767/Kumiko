import logging

from discord.ext import commands, tasks
from kumikocore import KumikoCore
from Libs.utils import calc_rank


class Tasks(commands.Cog, command_attrs=dict(hidden=True)):
    """Tasks that run in the background"""

    def __init__(self, bot: KumikoCore) -> None:
        self.bot = bot
        self.pool = self.bot.pool
        self.logger = logging.getLogger("discord")
        self.update_item_stock.start()
        self.update_job_pay.start()

    async def cog_unload(self):
        self.update_item_stock.stop()
        self.update_job_pay.stop()

    @tasks.loop(hours=1.0)
    async def update_item_stock(self) -> None:
        """The internal task of just updating the stocked items

        In this version, whether or not the item is bought is not taken into account. In future versions, that will be needed.

        The way it works is this:

        1. Get all of the items from the database (owned and not owned)
        2. Take the restock amount, and then add it to the current amount

        Prepared statements are used ofc.
        """
        # I know this is bad, but this needs to be addressed in a different update
        # Every single item, including owned ones will get update.
        # For now, i'll leave for now
        # By design, we quite literally want to restock every single one
        # The items now don't have owners
        getItems = """
        SELECT eco_item.id, eco_item.amount, eco_item.restock_amount
        FROM eco_item_lookup
        INNER JOIN eco_item ON eco_item.id = eco_item_lookup.item_id;
        """
        updateStock = """
        UPDATE eco_item
        SET amount = amount + $2
        WHERE id = $1;
        """
        async with self.pool.acquire() as conn:
            smt = await conn.prepare(getItems)
            async with conn.transaction():
                async for row in smt.cursor():
                    if row is not None:
                        record = dict(row)
                        await conn.execute(
                            updateStock, record["id"], record["restock_amount"]
                        )

    @tasks.loop(hours=1.0)
    async def update_job_pay(self) -> None:
        """The internal task of updating jobs every hour

        The way it works is a three step process:

        1. Get all of the user's id within the database. It is guaranteed that all users in that table have an "account" already.
        2. Sum the pay amount of all of the jobs that the user is associated with
        3. Check if the predicted rank is higher than the current rank.
            a) If it is, update the rank and add the petals. If it isn't, just add the petals

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
        updateRankAndPetalsQuery = """
        UPDATE eco_user
        SET rank = $2, petals = petals + $3
        WHERE id = $1;
        """
        async with self.pool.acquire() as conn:
            smt = await conn.prepare("SELECT id, rank, petals FROM eco_user")
            sumDataSmt = await conn.prepare(sumDataQuery)
            async with conn.transaction():
                async for record in smt.cursor():
                    fetchedRecord = dict(record)
                    total = await sumDataSmt.fetchval(fetchedRecord["id"])
                    if total is not None:
                        predictedRank = calc_rank(fetchedRecord["petals"] + total)
                        if predictedRank > fetchedRecord["rank"]:
                            await conn.execute(
                                updateRankAndPetalsQuery,
                                fetchedRecord["id"],
                                predictedRank,
                                total,
                            )
                        else:
                            await conn.execute(updateQuery, fetchedRecord["id"], total)

    @update_job_pay.error
    async def on_update_pay_error(self, error) -> None:
        self.logger.exception(f"Error in update_pay: {error}")


async def setup(bot: KumikoCore) -> None:
    await bot.add_cog(Tasks(bot))
