from typing import Dict, List, Union

import asyncpg


async def getPinText(
    id: int, pin_name: str, pool: asyncpg.Pool
) -> Union[str, List[Dict[str, str]], None]:
    """Gets a tag from the database.

    Args:
        id (int): Guild ID
        tag_name (str): Tag name
        pool (asyncpg.Pool): Database pool

    Returns:
        Union[str, None]: The tag content or None if it doesn't exist
    """
    sqlQuery = """
    SELECT pin.content
    FROM pin_lookup
    INNER JOIN pin ON pin.id = pin_lookup.pin_id
    WHERE pin_lookup.guild_id=$1 AND LOWER(pin_lookup.name)=$2 OR LOWER($2) = ANY(aliases); 
    """
    async with pool.acquire() as conn:
        res = await conn.fetchval(sqlQuery, id, pin_name)
        if res is None:
            query = """
            SELECT     pin_lookup.name
            FROM       pin_lookup
            WHERE      pin_lookup.guild_id=$1 AND pin_lookup.name % $2 OR $2 = ANY(aliases)
            ORDER BY   similarity(pin_lookup.name, $2) DESC
            LIMIT 5;
            """
            newRes = await conn.fetch(query, id, pin_name)
            if newRes is None or len(newRes) == 0:
                return None

            return [dict(row) for row in newRes]
        return res


async def getPinInfo(id: int, pin_name: str, pool: asyncpg.Pool) -> Union[Dict, None]:
    """Gets the info from an pin

    Args:
        id (int): Guild ID
        pin_name (str): The name of the pin
        pool (asyncpg.Pool): Asyncpg connection pool

    Returns:
        Union[Dict, None]: The pin info or None if it doesn't exist
    """
    query = """
    SELECT pin.name, pin.content, pin.created_at, pin.author_id, pin_lookup.aliases
    FROM pin_lookup
    INNER JOIN pin ON pin.id = pin_lookup.pin_id
    WHERE pin_lookup.guild_id=$1 AND LOWER(pin_lookup.name)=$2 OR LOWER(pin_lookup.name) = ANY(aliases);
    """
    res = await pool.fetchrow(query, id, pin_name)
    if res is None:
        return None
    return dict(res)


async def createPin(
    author_id: int, guild_id: int, pool: asyncpg.Pool, name: str, content: str
) -> str:
    """Creates a pin from the given info

    Args:
        author_id (int): The user's ID
        guild_id (int): The guild's ID
        pool (asyncpg.Pool): Asyncpg connection pool
        name (str): The name of the pin
        content (str): The contents of the pin

    Returns:
        str: The status of whether it was successful or not
    """

    query = """WITH pin_insert AS (
            INSERT INTO pin (author_id, guild_id, name, content) 
            VALUES ($1, $2, $3, $4)
            RETURNING id
        )
        INSERT INTO pin_lookup (name, owner_id, guild_id, pin_id)
        VALUES ($3, $1, $2, (SELECT id FROM pin_insert));
    """
    async with pool.acquire() as conn:
        tr = conn.transaction()
        await tr.start()
        try:
            await conn.execute(
                query,
                author_id,
                guild_id,
                name,
                content,
            )
        except asyncpg.UniqueViolationError:
            await tr.rollback()
            return f"The pin (`{name}`) already exists."
        except Exception:
            await tr.rollback()
            return "Could not create pin"
        else:
            await tr.commit()
            return f"Pin `{name}` successfully created"


async def editPin(
    guild_id: int, author_id: int, pool: asyncpg.Pool, name: str, content: str
) -> str:
    query = """
    UPDATE pin
    SET content = $1
    WHERE guild_id = $3 AND LOWER(pin.name) = $2 AND author_id = $4;
    """
    status = await pool.execute(query, content, name, guild_id, author_id)
    return status


async def getAllPins(guild_id: int, pool: asyncpg.Pool):
    query = """
    SELECT pin.id, pin.name, pin_lookup.aliases, pin.content, pin.created_at, pin.author_id
    FROM pin_lookup
    INNER JOIN pin ON pin.id = pin_lookup.pin_id
    WHERE pin_lookup.guild_id=$1;
    """
    async with pool.acquire() as conn:
        rows = await conn.fetch(query, guild_id)
        if rows is None:
            return []
        return rows


async def getOwnedPins(author_id: int, guild_id: int, pool: asyncpg.Pool):
    query = """
    SELECT pin.name, pin.id
    FROM pin_lookup
    INNER JOIN pin ON pin.id = pin_lookup.pin_id
    WHERE pin_lookup.guild_id=$1 AND pin_lookup.owner_id=$2;
    """
    async with pool.acquire() as conn:
        rows = await conn.fetch(query, guild_id, author_id)
        if rows is None:
            return []
        return rows
