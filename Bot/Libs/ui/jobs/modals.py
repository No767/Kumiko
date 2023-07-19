import asyncpg
import discord
from Libs.cog_utils.jobs import updateJob


class CreateJob(discord.ui.Modal, title="Create Job"):
    def __init__(self, pool: asyncpg.pool.Pool, required_rank: int, pay: int) -> None:
        super().__init__()
        self.pool: asyncpg.Pool = pool
        self.required_rank = required_rank
        self.pay = pay
        self.name = discord.ui.TextInput(
            label="Name",
            placeholder="Name of the job",
            min_length=1,
            max_length=255,
            row=0,
        )
        self.description = discord.ui.TextInput(
            label="Description",
            style=discord.TextStyle.long,
            placeholder="Description of the job",
            min_length=1,
            max_length=2000,
            row=1,
        )
        self.add_item(self.name)
        self.add_item(self.description)

    async def on_submit(self, interaction: discord.Interaction) -> None:
        # Ripped the whole thing from RDanny again...
        query = """
        WITH job_insert AS (
        INSERT INTO job (name, description, guild_id, creator_id, required_rank, pay_amount)
        VALUES ($3, $4, $1, $2, $5, $6)
        RETURNING id
        )
        INSERT into job_lookup (name, guild_id, creator_id, job_id)
        VALUES ($3, $1, $2, (SELECT id FROM job_insert));
        """
        async with self.pool.acquire() as conn:
            tr = conn.transaction()
            await tr.start()

            try:
                await conn.execute(
                    query,
                    interaction.guild.id,  # type: ignore
                    interaction.user.id,
                    self.name.value,
                    self.description.value,
                    self.required_rank,
                    self.pay,
                )
            except asyncpg.UniqueViolationError:
                await tr.rollback()
                await interaction.response.send_message("This job already exists.")
            except Exception:
                await tr.rollback()
                await interaction.response.send_message("Could not create job.")
            else:
                await tr.commit()
                await interaction.response.send_message(
                    f"Job {self.name} successfully created."
                )


class UpdateJobModal(discord.ui.Modal, title="Update Job"):
    def __init__(
        self, pool: asyncpg.pool.Pool, name: str, required_rank: int, pay: int
    ) -> None:
        super().__init__()
        self.pool: asyncpg.Pool = pool
        self.name = name
        self.required_rank = required_rank
        self.pay = pay
        self.description = discord.ui.TextInput(
            label="Description",
            style=discord.TextStyle.long,
            placeholder="Description of the job",
            min_length=1,
            max_length=2000,
            row=1,
        )
        self.add_item(self.description)

    async def on_submit(self, interaction: discord.Interaction) -> None:
        status = await updateJob(interaction.user.id, interaction.guild.id, self.pool, self.name, self.description.value, self.required_rank, self.pay)  # type: ignore
        if status[-1] == 0:
            await interaction.response.send_message(
                "You either don't own this job or the job doesn't exist. Try again."
            )
            return
        await interaction.response.send_message(
            f"Successfully updated the job `{self.name}` (RR: {self.required_rank}, Pay: {self.pay})"
        )
        return
