from typing import Union

import asyncpg


async def createJob(
    author_id: int,
    guild_id: int,
    pool: asyncpg.Pool,
    name: str,
    content: str,
    required_rank: int,
    pay: int,
):
    query = """
    WITH job_insert AS (
        INSERT INTO job (name, description, guild_id, creator_id, required_rank, pay_amount)
        VALUES ($3, $4, $1, $2, $5, $6)
        RETURNING id
    )
    INSERT into job_lookup (name, guild_id, creator_id, job_id)
    VALUES ($3, $1, $2, (SELECT id FROM job_insert));
    """
    async with pool.acquire() as conn:
        tr = conn.transaction()
        await tr.start()
        try:
            await conn.execute(
                query, guild_id, author_id, name, content, required_rank, pay
            )
        except asyncpg.UniqueViolationError:
            await tr.rollback()
            return "This job already exists"
        except Exception:
            await tr.rollback()
            return "Could not create job"
        else:
            await tr.commit()
            return f"Job {name} successfully created"


async def updateJob(
    author_id: int,
    guild_id: int,
    pool: asyncpg.Pool,
    name: str,
    description: str,
    required_rank: int,
    pay: int,
):
    query = """
    UPDATE job
    SET description = $1, required_rank = $2, pay_amount = $3
    WHERE guild_id = $4 AND LOWER(job.name) = $5 AND creator_id = $6;
    """
    status = await pool.execute(
        query, description, required_rank, pay, guild_id, name, author_id
    )
    return status


async def submitJobApp(
    owner_id: Union[int, None],
    guild_id: int,
    name: str,
    listed_status: bool,
    pool: asyncpg.Pool,
) -> str:
    query = """
    WITH job_update AS (
        UPDATE job
        SET worker_id = $1
        WHERE guild_id = $2 AND name = $3
        RETURNING id
    )
    UPDATE job_lookup
    SET worker_id = $1, listed = $4
    WHERE guild_id = $2 AND job_id = (SELECT id FROM job_update);
    """
    async with pool.acquire() as conn:
        tr = conn.transaction()
        await tr.start()
        try:
            await conn.execute(query, owner_id, guild_id, name.lower(), listed_status)  # type: ignore
        except asyncpg.UniqueViolationError:
            await tr.rollback()
            return "The job is already taken. Please apply for another one"
        else:
            await tr.commit()
            return f"Successfully {'quit' if listed_status is True else 'applied'} the job!"
