import asyncio
from typing import Dict

import discord
from discord import app_commands
from discord.ext import commands
from kumikocore import KumikoCore
from Libs.cog_utils.jobs import createJob, updateJob
from Libs.ui.jobs import (
    CreateJob,
    DeleteJobViaIDView,
    DeleteJobView,
    JobPages,
    PurgeJobsView,
    UpdateJobModal,
)
from Libs.utils import ConfirmEmbed, JobName
from Libs.utils.pages import EmbedListSource, KumikoPages
from typing_extensions import Annotated


class Jobs(commands.Cog):
    """Module for handling jobs for Kumiko's economy module"""

    def __init__(self, bot: KumikoCore) -> None:
        self.bot = bot
        self.pool = self.bot.pool
        self._reserved_jobs_being_made: Dict[int, set[str]] = {}

    def is_job_being_made(self, guild_id: int, name: str) -> bool:
        try:
            being_made = self._reserved_jobs_being_made[guild_id]
        except KeyError:
            return False
        else:
            return name.lower() in being_made

    def add_in_progress_job(self, guild_id: int, name: str) -> None:
        tags = self._reserved_jobs_being_made.setdefault(guild_id, set())
        tags.add(name.lower())

    def remove_in_progress_job(self, guild_id: int, name: str) -> None:
        try:
            being_made = self._reserved_jobs_being_made[guild_id]
        except KeyError:
            return

        being_made.discard(name.lower())
        if len(being_made) == 0:
            del self._reserved_jobs_being_made[guild_id]

    @property
    def display_emoji(self) -> discord.PartialEmoji:
        return discord.PartialEmoji(name="\U0001f4bc")

    @commands.hybrid_group(name="jobs", fallback="list")
    @app_commands.describe(compact="Whether to show a compacted page or not")
    async def jobs(self, ctx: commands.Context, compact: bool = False) -> None:
        """Lists all available jobs in your server"""
        sql = """
        SELECT job.id, job.name, job.description, job.required_rank, job.pay_amount
        FROM job_lookup
        INNER JOIN job ON job.id = job_lookup.job_id
        WHERE job_lookup.guild_id = $1 AND job_lookup.listed = $2;
        """
        results = await self.pool.fetch(sql, ctx.guild.id, True)  # type: ignore

        if len(results) == 0:
            await ctx.send(
                "There are no listed jobs in this server! Create one to get started!"
            )
            return
        if compact:
            pages = JobPages(entries=results, ctx=ctx, per_page=10)
            await pages.start()
        else:
            dataList = [
                {
                    "title": row["name"],
                    "description": row["description"],
                    "fields": [
                        {"name": "ID", "value": row["id"], "inline": True},
                        {
                            "name": "Required Rank",
                            "value": row["required_rank"],
                            "inline": True,
                        },
                        {
                            "name": "Pay Amount",
                            "value": row["pay_amount"],
                            "inline": True,
                        },
                    ],
                }
                for row in results
            ]
            pages = KumikoPages(EmbedListSource(dataList, per_page=1), ctx=ctx)
            await pages.start()

    @jobs.command(name="create")
    @app_commands.describe(
        required_rank="The required rank or higher to obtain the job",
        pay="The base pay required for the job",
    )
    async def create(
        self, ctx: commands.Context, required_rank: int = 0, pay: int = 15
    ) -> None:
        """Create a job for your server"""
        if ctx.interaction is not None:
            createPinModal = CreateJob(self.pool, required_rank, pay)
            await ctx.interaction.response.send_modal(createPinModal)
            return

        await ctx.send("What would you like the job's name to be?")

        converter = JobName()
        original = ctx.message

        def check(msg):
            return msg.author == ctx.author and ctx.channel == msg.channel

        try:
            name = await self.bot.wait_for("message", timeout=30.0, check=check)
        except asyncio.TimeoutError:
            await ctx.send("You took long. Goodbye.")
            return

        try:
            ctx.message = name
            name = await converter.convert(ctx, name.content)
        except commands.BadArgument as e:
            await ctx.send(f'{e}. Redo the command "{ctx.prefix}jobs make" to retry.')
            return
        finally:
            ctx.message = original

        if self.is_job_being_made(ctx.guild.id, name):  # type: ignore
            await ctx.send(
                "Sorry. This job is currently being made by someone. "
                f'Redo the command "{ctx.prefix}jobs make" to retry.'
            )
            return

        query = """SELECT 1 FROM job WHERE guild_id=$1 AND LOWER(name)=$2;"""
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow(query, ctx.guild.id, name.lower())  # type: ignore
            if row is not None:
                await ctx.send(
                    "Sorry. A job with that name already exists. "
                    f'Redo the command "{ctx.prefix}jobs make" to retry.'
                )
                return None

        self.add_in_progress_job(ctx.guild.id, name)  # type: ignore
        await ctx.send(
            f"Neat. So the name is {name}. What about the job's description? "
            f"**You can type `abort` to abort the pin make process.**"
        )

        try:
            msg = await self.bot.wait_for("message", check=check, timeout=350.0)
        except asyncio.TimeoutError:
            self.remove_in_progress_job(ctx.guild.id, name)  # type: ignore
            await ctx.send("You took too long. Goodbye.")
            return

        if msg.content == "abort":
            self.remove_in_progress_job(ctx.guild.id, name)  # type: ignore
            await ctx.send("Aborting.")
            return
        elif msg.content:
            clean_content = await commands.clean_content().convert(ctx, msg.content)
        else:
            # fast path I guess?
            clean_content = msg.content

        if msg.attachments:
            clean_content = f"{clean_content}\n{msg.attachments[0].url}"

        if len(clean_content) > 2000:
            await ctx.send("Job description is a maximum of 2000 characters.")
            return

        try:
            status = await createJob(ctx.author.id, ctx.guild.id, self.pool, name, clean_content, required_rank, pay)  # type: ignore
            await ctx.send(status)
        finally:
            self.remove_in_progress_job(ctx.guild.id, name)  # type: ignore

    @jobs.command(name="update")
    @app_commands.describe(
        name="The name of the job to update",
        required_rank="The mew required rank or higher to obtain the job",
        pay="The new base pay required for the job",
    )
    async def update(
        self,
        ctx: commands.Context,
        name: Annotated[str, commands.clean_content],
        required_rank: int,
        pay: int,
    ) -> None:
        """Updates an owned job with new information"""
        if ctx.interaction is not None:
            updateJobModal = UpdateJobModal(self.pool, name, required_rank, pay)
            await ctx.interaction.response.send_modal(updateJobModal)
            return

        def check(msg):
            return msg.author == ctx.author and ctx.channel == msg.channel

        await ctx.send(
            "What's the description for your job going to be?"
            "Note that this new description replaces the old one."
        )
        try:
            msg = await self.bot.wait_for("message", check=check, timeout=350.0)
        except asyncio.TimeoutError:
            self.remove_in_progress_job(ctx.guild.id, name)  # type: ignore
            await ctx.send("You took too long. Goodbye.")
            return

        if msg.content:
            clean_content = await commands.clean_content().convert(ctx, msg.content)
        else:
            clean_content = msg.content

        if msg.attachments:
            clean_content = f"{clean_content}\n{msg.attachments[0].url}"

        if len(clean_content) > 2000:
            await ctx.send("Job description is a maximum of 2000 characters.")
            return

        status = await updateJob(ctx.author.id, ctx.guild.id, self.pool, name, clean_content, required_rank, pay)  # type: ignore
        if status[-1] == 0:
            await ctx.send(
                "You either don't own this job or the job doesn't exist. Try again."
            )
            return
        await ctx.send(
            f"Successfully updated the job `{name}` (RR: {required_rank}, Pay: {pay})"
        )
        return

    @jobs.command(name="delete")
    @app_commands.describe(name="The name of the job to delete")
    async def delete(
        self, ctx: commands.Context, name: Annotated[str, commands.clean_content]
    ) -> None:
        """Deletes a job by name. You can only delete your own jobs."""
        view = DeleteJobView(self.pool, name)
        embed = ConfirmEmbed()
        embed.description = f"Are you sure you want to delete the job `{name}`?"
        await ctx.send(embed=embed, view=view)

    @jobs.command(name="delete-id")
    @app_commands.describe(id="The ID of the job to delete")
    async def delete_via_id(self, ctx: commands.Context, id: int) -> None:
        """Deletes the job via the job ID"""
        view = DeleteJobViaIDView(self.pool, id)
        embed = ConfirmEmbed()
        embed.description = f"Are you sure you want to delete the job? (ID: `{id}`)?"
        await ctx.send(embed=embed, view=view)

    @jobs.command(name="purge")
    async def purge(self, ctx: commands.Context) -> None:
        """Purges all jobs that you own"""
        view = PurgeJobsView(self.pool)
        embed = ConfirmEmbed()
        embed.description = "Are you sure you want to delete all jobs that you own?"
        await ctx.send(embed=embed, view=view)

    @jobs.command(name="file")
    @app_commands.describe(name="The name of the job to file")
    async def file(
        self, ctx: commands.Context, name: Annotated[str, commands.clean_content]
    ) -> None:
        """Files (publicly lists) a job for general availability. This must be one that you own"""
        query = """
        UPDATE job_lookup
        SET listed = $4
        WHERE guild_id=$1 AND owner_id=$2 AND LOWER(name)=$3;
        """
        status = await self.pool.execute(query, ctx.guild.id, ctx.author.id, name.lower(), True)  # type: ignore
        if status[-1] == 0:
            await ctx.send(
                "You either don't own this job or the job doesn't exist. Try again."
            )
        else:
            await ctx.send(f"Successfully filed job `{name}` for general availability.")

    @jobs.command(name="unfile")
    @app_commands.describe(name="The name of the job to un-file")
    async def unfile(
        self, ctx: commands.Context, name: Annotated[str, commands.clean_content]
    ) -> None:
        """Un-files a job for general availability. This must be one that you own"""
        query = """
        UPDATE job_lookup
        SET listed = $4
        WHERE guild_id=$1 AND owner_id=$2 AND LOWER(name)=$3;
        """
        status = await self.pool.execute(query, ctx.guild.id, ctx.author.id, name.lower(), False)  # type: ignore
        if status[-1] == 0:
            await ctx.send(
                "You either don't own this job or the job doesn't exist. Try again."
            )
        else:
            await ctx.send(
                f"Successfully un-filed job `{name}` for general availability."
            )


async def setup(bot: KumikoCore) -> None:
    await bot.add_cog(Jobs(bot))
