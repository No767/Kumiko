from typing import Dict, List, Union

import asyncpg


async def getPinText(
    id: int, pin_name: str, pool: asyncpg.Pool
) -> Union[Dict, List[Dict], None]:
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
    WHERE pin_lookup.guild_id=$1 AND LOWER(pin_lookup.name)=$2;
    """
    async with pool.acquire() as conn:
        res = await conn.fetchval(sqlQuery, id, pin_name)
        if res is None:
            query = """
            SELECT     pin_lookup.name
            FROM       pin_lookup
            WHERE      pin_lookup.guild_id=$1 AND pin_lookup.name % $2
            ORDER BY   similarity(pin_lookup.name, $2) DESC
            LIMIT 5;
            """
            newRes = await conn.fetch(query, id, pin_name)
            if newRes is None or len(newRes) == 0:
                return None

            return [dict(row) for row in newRes]
        return res


async def getPinInfo(id: int, pin_name: str, pool: asyncpg.Pool) -> Union[Dict, None]:
    query = """
    SELECT pin.name, pin.content, pin.created_at, pin.author_id
    FROM pin_lookup
    INNER JOIN pin ON pin.id = pin_lookup.pin_id
    WHERE pin_lookup.guild_id=$1 AND LOWER(pin_lookup.name)=$2;
    """
    async with pool.acquire() as conn:
        res = await conn.fetchrow(query, id, pin_name)
        if res is None:
            return None
        return dict(res)
