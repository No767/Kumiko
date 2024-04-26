import asyncio
from typing import Dict

import discord
from discord import app_commands
from discord.ext import commands
from kumikocore import KumikoCore
from libs.cog_utils.economy import check_economy_enabled
from libs.cog_utils.jobs import (
    JobListFlags,
    JobOutputFlags,
    create_job,
    create_job_output_item,
    format_job_options,
    get_job,
    submit_job_app,
    update_job,
)
from libs.ui.jobs import (
    CreateJob,
    CreateJobOutputItemModal,
    DeleteJobViaIDView,
    DeleteJobView,
    JobPages,
    PurgeJobsView,
    UpdateJobModal,
)
from libs.utils import ConfirmEmbed, Embed, MessageConstants
from libs.utils.pages import EmbedListSource, KumikoPages
from typing_extensions import Annotated


class JobName(commands.clean_content):
    def __init__(self, *, lower: bool = False):
        self.lower: bool = lower
        super().__init__()

    async def convert(self, ctx: commands.Context, argument: str) -> str:
        converted = await super().convert(ctx, argument)
        lower = converted.lower().strip()

        if len(lower) > 100:
            raise commands.BadArgument("Job name is a maximum of 100 characters.")

        first_word, _, _ = lower.partition(" ")

        root: commands.GroupMixin = ctx.bot.get_command("jobs")
        if first_word in root.all_commands:
            raise commands.BadArgument("This Job name starts with a reserved word.")

        return converted.strip() if not self.lower else lower


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

    async def cog_check(self, ctx: commands.Context) -> bool:
        return await check_economy_enabled(ctx)

    @commands.hybrid_group(name="jobs", fallback="list")
    async def jobs(self, ctx: commands.Context, flags: JobListFlags) -> None:
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
        if flags.compact is True:
            pages = JobPages(entries=results, ctx=ctx, per_page=10)
            await pages.start()
        else:
            data_list = [
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
            pages = KumikoPages(EmbedListSource(data_list, per_page=1), ctx=ctx)
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
            create_job_modal = CreateJob(ctx, self.pool, required_rank, pay)
            await ctx.interaction.response.send_modal(create_job_modal)
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
            await ctx.send(MessageConstants.TIMEOUT.value)
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
            status = await create_job(ctx.author.id, ctx.guild.id, self.pool, name, clean_content, required_rank, pay)  # type: ignore
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
            update_job_modal = UpdateJobModal(ctx, self.pool, name, required_rank, pay)
            await ctx.interaction.response.send_modal(update_job_modal)
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
            await ctx.send(MessageConstants.TIMEOUT.value)
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

        status = await update_job(ctx.author.id, ctx.guild.id, self.pool, name, clean_content, required_rank, pay)  # type: ignore
        if status[-1] == 0:
            await ctx.send(MessageConstants.NO_JOB.value)
            return
        await ctx.send(
            f"Successfully updated the job `{name}` (RR: {required_rank}, Pay: {pay})"
        )

    @jobs.command(name="delete")
    @app_commands.describe(name="The name of the job to delete")
    async def delete(
        self, ctx: commands.Context, name: Annotated[str, commands.clean_content]
    ) -> None:
        """Deletes a job by name. You can only delete your own jobs."""
        view = DeleteJobView(ctx, self.pool, name)
        embed = ConfirmEmbed()
        embed.description = f"Are you sure you want to delete the job `{name}`?"
        await ctx.send(embed=embed, view=view)

    @jobs.command(name="delete-id")
    @app_commands.describe(id="The ID of the job to delete")
    async def delete_via_id(self, ctx: commands.Context, id: int) -> None:
        """Deletes the job via the job ID"""
        view = DeleteJobViaIDView(ctx, self.pool, id)
        embed = ConfirmEmbed()
        embed.description = f"Are you sure you want to delete the job? (ID: `{id}`)?"
        await ctx.send(embed=embed, view=view)

    @jobs.command(name="purge")
    async def purge(self, ctx: commands.Context) -> None:
        """Purges all jobs that you own"""
        view = PurgeJobsView(ctx, self.pool)
        embed = ConfirmEmbed()
        embed.description = "Are you sure you want to delete all jobs that you own?"
        await ctx.send(embed=embed, view=view)

    @jobs.command(name="file")
    @app_commands.describe(name="The name of the job to file")
    async def file(
        self, ctx: commands.Context, *, name: Annotated[str, commands.clean_content]
    ) -> None:
        """Files (publicly lists) a job for general availability. This must be one that you own"""
        query = """
        UPDATE job_lookup
        SET listed = $4
        WHERE guild_id=$1 AND creator_id=$2 AND LOWER(name)=$3;
        """
        status = await self.pool.execute(query, ctx.guild.id, ctx.author.id, name.lower(), True)  # type: ignore
        if status[-1] == 0:
            await ctx.send(MessageConstants.NO_JOB.value)
        else:
            await ctx.send(f"Successfully filed job `{name}` for general availability.")

    @jobs.command(name="unfile")
    @app_commands.describe(name="The name of the job to un-file")
    async def unfile(
        self, ctx: commands.Context, *, name: Annotated[str, commands.clean_content]
    ) -> None:
        """Un-files a job for general availability. This must be one that you own"""
        query = """
        UPDATE job_lookup
        SET listed = $4
        WHERE guild_id=$1 AND creator_id=$2 AND LOWER(name)=$3;
        """
        status = await self.pool.execute(query, ctx.guild.id, ctx.author.id, name.lower(), False)  # type: ignore
        if status[-1] == 0:
            await ctx.send(MessageConstants.NO_JOB.value)
        else:
            await ctx.send(
                f"Successfully un-filed job `{name}` for general availability."
            )

    # Probably should make a custom converter for this

    @jobs.command(name="apply")
    @app_commands.describe(name="The name of the job to apply")
    async def apply(
        self, ctx: commands.Context, *, name: Annotated[str, commands.clean_content]
    ) -> None:
        """Apply for a job"""
        query = """
        SELECT COUNT(*) FROM job WHERE guild_id = $1 AND worker_id = $2;
        """
        async with self.pool.acquire() as conn:
            job_count = await conn.fetchval(query, ctx.guild.id, ctx.author.id)  # type: ignore
            rows = await conn.fetchrow("SELECT creator_id, worker_id FROM job WHERE guild_id = $1 AND name = $2;", ctx.guild.id, name.lower())  # type: ignore
            # customizable?
            if job_count > 3:
                await ctx.send("You can't have more than 3 jobs at a time!")
                return

            if dict(rows)["creator_id"] == ctx.author.id:
                await ctx.send("You can't apply for your own job!")
                return

            if dict(rows)["worker_id"] is not None:
                await ctx.send("This job is already taken!")
                return

            status = await submit_job_app(ctx.author.id, ctx.guild.id, name.lower(), False, conn)  # type: ignore
            await ctx.send(status)

    @jobs.command(name="quit")
    @app_commands.describe(name="The name of the job to quit")
    async def quit(
        self, ctx: commands.Context, *, name: Annotated[str, commands.clean_content]
    ) -> None:
        """Quit a current job that you have"""
        async with self.pool.acquire() as conn:
            rows = await conn.fetchrow("SELECT creator_id, worker_id FROM job WHERE guild_id = $1 AND name = $2;", ctx.guild.id, name.lower())  # type: ignore
            if dict(rows)["creator_id"] == ctx.author.id:
                await ctx.send("You can't apply for your own job!")
                return

            if dict(rows)["worker_id"] is None:
                await ctx.send("This job is available! Apply for it first!")
            else:
                status = await submit_job_app(None, ctx.guild.id, name.lower(), True, conn)  # type: ignore
                await ctx.send(status)

    @jobs.command(name="info")
    @app_commands.describe(name="The name of the job to get")
    async def info(
        self, ctx: commands.Context, *, name: Annotated[str, commands.clean_content]
    ) -> None:
        """Get info about a job"""
        job_results = await get_job(ctx.guild.id, name.lower(), self.pool)  # type: ignore
        if isinstance(job_results, list):
            await ctx.send(format_job_options(job_results) or "No jobs were found")
            return
        embed = Embed(title=job_results["name"], description=job_results["description"])  # type: ignore
        embed.add_field(name="Required Rank", value=job_results["required_rank"])  # type: ignore
        embed.add_field(name="Pay Amount", value=job_results["pay_amount"])  # type: ignore
        embed.set_footer(text=f"ID: {job_results['id']}")  # type: ignore
        await ctx.send(embed=embed)

    @jobs.command(name="search")
    @app_commands.describe(query="The name of the job to look for")
    async def search(
        self, ctx: commands.Context, *, query: Annotated[str, commands.clean_content]
    ) -> None:
        """Search for jobs that are available. These must be listed in order to show up"""
        if len(query) < 3:
            await ctx.send("The query must be at least 3 characters")
            return
        sql = """SELECT job.id, job.name, job.description, job.required_rank, job.pay_amount
                 FROM job_lookup
                 WHERE guild_id=$1 AND name % $2 AND listed = $3
                 ORDER BY similarity(name, $2) DESC
                 LIMIT 100;
              """
        rows = await self.pool.fetch(sql, ctx.guild.id, query, True)  # type: ignore
        if rows:
            pages = JobPages(entries=rows, ctx=ctx, per_page=10)
            await pages.start()
        else:
            await ctx.send("No jobs were found")

    @jobs.command(name="output", usage="<name> price: int amount_per_hour: int")
    @app_commands.describe(name="The name of the item that the job outputs")
    async def associate_item(
        self,
        ctx: commands.Context,
        name: Annotated[str, commands.clean_content],
        *,
        flags: JobOutputFlags,
    ) -> None:
        """Associate an item with the job's output. A job can only produce one item."""
        if ctx.interaction is not None:
            output_modal = CreateJobOutputItemModal(
                ctx, self.pool, name, flags.price, flags.amount_per_hour
            )
            await ctx.interaction.response.send_modal(output_modal)
            return

        def check(msg):
            return msg.author == ctx.author and ctx.channel == msg.channel

        await ctx.send("What's the description for your item going to be?")
        try:
            msg = await self.bot.wait_for("message", check=check, timeout=350.0)
        except asyncio.TimeoutError:
            self.remove_in_progress_job(ctx.guild.id, name)  # type: ignore
            await ctx.send(MessageConstants.TIMEOUT.value)
            return

        if msg.content:
            clean_content = await commands.clean_content().convert(ctx, msg.content)
        else:
            clean_content = msg.content

        if msg.attachments:
            clean_content = f"{clean_content}\n{msg.attachments[0].url}"

        if len(clean_content) > 2000:
            await ctx.send("Item description is a maximum of 2000 characters.")
            return

        status = await create_job_output_item(
            name=name,
            description=clean_content,
            price=flags.price,
            amount=flags.amount_per_hour,
            guild_id=ctx.guild.id,  # type: ignore
            worker_id=ctx.author.id,
            pool=self.pool,
        )
        if status[-1] != "0":
            await ctx.send(
                f"Successfully created the output item `{name}` (Price: {flags.price}, Amount Per Hour: {flags.amount_per_hour})"
            )
        else:
            await ctx.send("There was an error making it. Please try again")


async def setup(bot: KumikoCore) -> None:
    await bot.add_cog(Jobs(bot))
