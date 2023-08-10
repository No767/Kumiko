from typing import Any, Dict, List, Union

import asyncpg


async def get_item(
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
    query = """
    SELECT eco_item.id, eco_item.name, eco_item.description, eco_item.price, eco_item.amount, eco_item.created_at, eco_item.producer_id
    FROM eco_item_lookup
    INNER JOIN eco_item ON eco_item.id = eco_item_lookup.item_id
    WHERE eco_item_lookup.guild_id=$1 AND LOWER(eco_item_lookup.name)=$2; 
    """
    async with pool.acquire() as conn:
        res = await conn.fetchrow(query, id, item_name)
        if res is None:
            query = """
            SELECT     eco_item_lookup.name
            FROM       eco_item_lookup
            WHERE      eco_item_lookup.guild_id=$1 AND eco_item_lookup.name % $2
            ORDER BY   similarity(eco_item_lookup.name, $2) DESC
            LIMIT 5;
            """
            new_res = await conn.fetch(query, id, item_name)
            if new_res is None or len(new_res) == 0:
                return None

            return [dict(row) for row in new_res]
        return dict(res)


async def is_payment_valid(
    rows: Dict[str, Any],
    purchaser_id: int,
    requested_amount: int,
    conn: asyncpg.connection.Connection,
) -> bool:
    query = """
    SELECT petals
    FROM eco_user
    WHERE id = $1;
    """

    petals = await conn.fetchval(query, purchaser_id)
    if petals is None:
        return False

    total_price = rows["price"] * requested_amount
    stock_amt = rows["amount"]
    return (
        (petals >= total_price) and (requested_amount < stock_amt) and (stock_amt > 0)
    )


def format_item_options(rows: Union[List[Dict[str, str]], None]) -> str:
    """Format the rows to be sent to the user

    Args:
        rows (Union[List[Dict[str, str]], None]): Rows to format

    Returns:
        str: _Formatted string
    """
    if rows is None or len(rows) == 0:
        return "Item not found"

    names = "\n".join([row["name"] for row in rows])
    return f"Item not found. Did you mean:\n{names}"


async def create_purchase_item(
    guild_id: int,
    user_id: int,
    name: str,
    amount_remaining: int,
    taken_stock: int,
    conn: asyncpg.connection.Connection,
) -> str:
    query = """
    WITH item_update AS (
        UPDATE eco_item
        SET amount = $4
        WHERE guild_id = $1 AND name = $3
        RETURNING id
    )
    INSERT INTO user_inv (owner_id, guild_id, amount_owned, item_id)
    VALUES ($2, $1, $5, (SELECT id FROM item_update))
    ON CONFLICT (item_id) DO NOTHING;
    """
    status = await conn.execute(
        query, guild_id, user_id, name, amount_remaining, taken_stock
    )
    return status
