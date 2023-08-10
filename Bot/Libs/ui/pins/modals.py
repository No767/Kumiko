import asyncpg
import discord
from Libs.cog_utils.pins import edit_pin


class CreatePin(discord.ui.Modal, title="Create Pin"):
    def __init__(self, pool: asyncpg.pool.Pool) -> None:
        super().__init__()
        self.pool: asyncpg.Pool = pool
        self.name = discord.ui.TextInput(
            label="Name",
            placeholder="Name of the pin",
            min_length=1,
            max_length=255,
            row=0,
        )
        self.content = discord.ui.TextInput(
            label="Content",
            style=discord.TextStyle.long,
            placeholder="Content of the pin",
            min_length=1,
            max_length=2000,
            row=1,
        )
        self.add_item(self.name)
        self.add_item(self.content)

    async def on_submit(self, interaction: discord.Interaction) -> None:
        # Ripped the whole thing from RDanny again...
        query = """WITH pin_insert AS (
            INSERT INTO pin (author_id, guild_id, name, content) 
            VALUES ($1, $2, $3, $4)
            RETURNING id
        )
        INSERT INTO pin_lookup (name, owner_id, guild_id, pin_id)
        VALUES ($3, $1, $2, (SELECT id FROM pin_insert));
        """
        async with self.pool.acquire() as conn:
            tr = conn.transaction()
            await tr.start()

            try:
                await conn.execute(
                    query,
                    interaction.user.id,
                    interaction.guild.id,  # type: ignore
                    self.name.value,
                    self.content.value,
                )
            except asyncpg.UniqueViolationError:
                await tr.rollback()
                await interaction.response.send_message("This pin already exists.")
            except Exception:
                await tr.rollback()
                await interaction.response.send_message("Could not create pin.")
            else:
                await tr.commit()
                await interaction.response.send_message(
                    f"Pin {self.name} successfully created."
                )

    async def on_error(
        self, interaction: discord.Interaction, error: Exception
    ) -> None:
        await interaction.response.send_message(
            f"An error occurred ({error.__class__.__name__})", ephemeral=True
        )


class PinEditModal(discord.ui.Modal, title="Edit Pin"):
    def __init__(self, pool: asyncpg.Pool, name: str) -> None:
        super().__init__()
        self.pool: asyncpg.Pool = pool
        self.name = name
        self.content = discord.ui.TextInput(
            label="Content",
            style=discord.TextStyle.long,
            placeholder="Content of the pin",
            min_length=1,
            max_length=2000,
            row=1,
        )
        self.add_item(self.content)

    async def on_submit(self, interaction: discord.Interaction) -> None:
        guild_id = interaction.guild.id  # type: ignore
        user_id = interaction.user.id
        res = await edit_pin(
            guild_id, user_id, self.pool, self.name, self.content.value
        )
        if res[-1] == "0":
            await interaction.response.send_message(
                "Could not edit pin. Are you sure you own it?"
            )
            self.stop()
        else:
            await interaction.response.send_message("Successfully edited pin")

    async def on_error(
        self, interaction: discord.Interaction, error: Exception
    ) -> None:
        await interaction.response.send_message(
            f"An error occurred ({error.__class__.__name__})", ephemeral=True
        )
        self.stop()
