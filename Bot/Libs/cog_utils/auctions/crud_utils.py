from typing import Any, Dict, Optional

import asyncpg


async def is_auction_valid(
    rows: Dict[str, Any],
    user_id: int,
    requested_amount: int,
    conn: asyncpg.connection.Connection,
) -> bool:
    query = """
    SELECT petals
    FROM eco_user
    WHERE id = $1;
    """

    petals = await conn.fetchval(query, user_id)
    if petals is None:
        return False

    total_amount = rows["amount_owned"]
    print(total_amount)
    return (petals >= 5) and (requested_amount <= total_amount)


async def create_auction(
    guild_id: int,
    user_id: int,
    amount_requested: int,
    item_id: Optional[int],
    item_name: Optional[str],
    pool: asyncpg.Pool,
):
    take_from_base_fee = """
    UPDATE eco_user
    SET petals = petals - $2
    WHERE id = $1;
    """
    get_item_from_inv = """
    SELECT eco_item.price, user_inv.guild_id, user_inv.owner_id, user_inv.amount_owned, user_inv.item_id
    FROM eco_item
    INNER JOIN user_inv ON user_inv.item_id = eco_item.id
    WHERE user_inv.owner_id = $1 AND user_inv.guild_id = $2 AND eco_item.name = $3 OR eco_item.id = $4;
    """
    insert_into_auctions = """
    WITH deplete_from_inv AS (
        UPDATE user_inv
        SET amount_owned = amount_owned - $4
        WHERE owner_id = $1 AND guild_id = $2 AND item_id = $3
        RETURNING id
    )
    INSERT INTO auction_house (item_id, user_id, guild_id, amount_listed, listed_price)
    VALUES ($3, $1, $2, $4, $5)
    ON CONFLICT (item_id, user_id) DO UPDATE
    SET amount_listed = auction_house.amount_listed + $4;
    """
    insert_into_bridge = """
    INSERT INTO ah_user_bridge (ah_item_id, user_id)
    VALUES ($1, $2)
    ON CONFLICT (ah_item_id, user_id) DO NOTHING;
    """
    async with pool.acquire() as conn:
        rows = await conn.fetchrow(
            get_item_from_inv, user_id, guild_id, item_name, item_id
        )
        if rows is None:
            return "The item that you are trying to list is not in your inventory"
        records = dict(rows)
        listedPrice = records["price"]
        await conn.execute(take_from_base_fee, user_id, 5)
        # print(await is_auction_valid(records, user_id, amount_requested, conn))
        # if await is_auction_valid(records, user_id, amount_requested, conn):
        async with conn.transaction():
            await conn.execute(
                insert_into_auctions,
                user_id,
                guild_id,
                records["item_id"],
                amount_requested,
                listedPrice,
            )
            await conn.execute(insert_into_bridge, records["item_id"], user_id)
            return "Successfully listed your item into the auction house"
        # else:
        #     return "You have an invalid attempted listing"
