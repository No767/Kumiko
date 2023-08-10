from typing import Dict, List, TypedDict, Union

import asyncpg


class JobResults(TypedDict):
    id: int
    name: str
    description: str
    required_rank: int
    pay_amount: int
    listed: bool


async def create_job(
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


async def update_job(
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


async def submit_job_app(
    owner_id: Union[int, None],
    guild_id: int,
    name: str,
    listed_status: bool,
    connection: asyncpg.Connection,
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
    tr = connection.transaction()
    await tr.start()
    try:
        await connection.execute(query, owner_id, guild_id, name.lower(), listed_status)
    except asyncpg.UniqueViolationError:
        await tr.rollback()
        return "The job is already taken. Please apply for another one"
    else:
        await tr.commit()
        return f"Successfully {'quit' if listed_status is True else 'applied'} the job!"


async def get_job(
    id: int, job_name: str, pool: asyncpg.Pool
) -> Union[Dict, List[Dict[str, str]], None]:
    """Gets a job from the database.

    Args:
        id (int): Guild ID
        job_name (str): Job name
        pool (asyncpg.Pool): Database pool

    Returns:
        Union[str, None]: The job details or None if it doesn't exist
    """
    query = """
    SELECT job.id, job.name, job.description, job.required_rank, job.pay_amount, job_lookup.listed
    FROM job_lookup
    INNER JOIN job ON job.id = job_lookup.job_id
    WHERE job_lookup.guild_id=$1 AND LOWER(job_lookup.name)=$2; 
    """
    async with pool.acquire() as conn:
        res = await conn.fetchrow(query, id, job_name)
        if res is None:
            query = """
            SELECT     job_lookup.name
            FROM       job_lookup
            WHERE      job_lookup.guild_id=$1 AND job_lookup.name % $2
            ORDER BY   similarity(job_lookup.name, $2) DESC
            LIMIT 5;
            """
            new_res = await conn.fetch(query, id, job_name)
            if new_res is None or len(new_res) == 0:
                return None

            return [dict(row) for row in new_res]
        return dict(res)


async def create_job_link(
    worker_id: int, item_id: int, job_id: int, conn: asyncpg.connection.Connection
):
    sql = """
    INSERT INTO job_output (worker_id, item_id, job_id)
    VALUES ($1, $2, $3);
    """
    status = await conn.execute(sql, worker_id, item_id, job_id)
    return status


async def create_job_output_item(
    name: str,
    description: str,
    price: int,
    amount: int,
    guild_id: int,
    worker_id: int,
    pool: asyncpg.Pool,
):
    # I have committed way too much sins
    # TODO - Add an upsert in this area
    sql = """
    WITH item_insert AS (
        INSERT INTO eco_item (guild_id, name, description, price, amount, restock_amount, producer_id)
        VALUES ($1, $2, $3, $4, $5, $6, $7)
        RETURNING id
    )
    INSERT INTO eco_item_lookup (name, guild_id, producer_id, item_id)
    VALUES ($2, $1, $7, (SELECT id FROM item_insert))
    """
    async with pool.acquire() as conn:
        tr = conn.transaction()
        await tr.start()

        try:
            status = await conn.execute(
                sql, guild_id, name, description, price, 1, amount, worker_id
            )
        except asyncpg.UniqueViolationError:
            await tr.rollback()
            return "This item already exists"
        else:
            await tr.commit()
            return status
