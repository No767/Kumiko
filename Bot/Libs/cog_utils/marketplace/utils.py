from typing import Dict, List, Union

import asyncpg


async def getItem(
    id: int, item_name: str, pool: asyncpg.Pool
) -> Union[Dict, List[Dict[str, str]], None]:
    """Gets a item from the database.

    Args:
        id (int): Guild ID
        item_name (str): Job name
        pool (asyncpg.Pool): Database pool

    Returns:
        Union[str, None]: The item details or None if it doesn't exist
    """
    sqlQuery = """
    SELECT eco_item.id, eco_item.name, eco_item.description, eco_item.price, eco_item.amount, eco_item.producer_id
    FROM eco_item_lookup
    INNER JOIN eco_item ON eco_item.id = eco_item_lookup.item_id
    WHERE eco_item_lookup.guild_id=$1 AND LOWER(eco_item_lookup.name)=$2; 
    """
    async with pool.acquire() as conn:
        res = await conn.fetchrow(sqlQuery, id, item_name)
        if res is None:
            query = """
            SELECT     eco_item_lookup.name
            FROM       eco_item_lookup
            WHERE      eco_item_lookup.guild_id=$1 AND eco_item_lookup.name % $2
            ORDER BY   similarity(eco_item_lookup.name, $2) DESC
            LIMIT 5;
            """
            newRes = await conn.fetch(query, id, item_name)
            if newRes is None or len(newRes) == 0:
                return None

            return [dict(row) for row in newRes]
        return dict(res)
