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
        INSERT INTO job (name, description, guild_id, owner_id, required_rank, pay_amount)
        VALUES ($3, $4, $1, $2, $5, $6)
        RETURNING id
    )
    INSERT into job_lookup (name, guild_id, owner_id, job_id)
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
    WHERE guild_id = $4 AND LOWER(job.name) = $5 AND owner_id = $6;
    """
    status = await pool.execute(
        query, description, required_rank, pay, guild_id, name, author_id
    )
    return status
