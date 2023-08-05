from typing import Any, Dict, List, Optional, Union

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

    amount_owned = rows["amount_owned"]
    return (petals >= 5) and (requested_amount <= amount_owned)


async def create_auction(
    guild_id: int,
    user_id: int,
    amount_requested: int,
    item_id: Optional[int],
    item_name: Optional[str],
    pool: asyncpg.Pool,
) -> str:
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
    get_new_item_listed = """
    SELECT id 
    FROM auction_house
    WHERE user_id = $1 AND guild_id = $2 AND item_id = $3;
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
        if await is_auction_valid(records, user_id, amount_requested, conn):
            async with conn.transaction():
                status = await conn.execute(
                    insert_into_auctions,
                    user_id,
                    guild_id,
                    records["item_id"],
                    amount_requested,
                    listedPrice,
                )
                if status[-1] != "0":
                    new_ah_item_id = await conn.fetchval(
                        get_new_item_listed, user_id, guild_id, records["item_id"]
                    )
                    if new_ah_item_id is None:
                        return "The item is not listed somehow. This is usually due a bug in the system. Contact the dev for more info"
                    await conn.execute(insert_into_bridge, new_ah_item_id, user_id)
                    return "Successfully listed your item into the auction house"
                return "Successfully updated your listing"
        else:
            return "You either do not have enough petals (5 is required to list) or you own less than what you are requesting to list"


async def delete_auction(
    guild_id: int,
    user_id: int,
    pool: asyncpg.Pool,
    item_name: Optional[str] = None,
    item_id: Optional[int] = None,
) -> str:
    get_name_from_id = """
    SELECT id FROM eco_item
    WHERE name = $1 AND guild_id = $2;
    """

    get_item_info = """
    SELECT auction_house.id, auction_house.item_id, auction_house.amount_listed, auction_house.user_id, user_inv.amount_owned
    FROM auction_house
    INNER JOIN user_inv ON user_inv.item_id = auction_house.item_id AND user_inv.owner_id = auction_house.user_id
    WHERE auction_house.user_id = $1 AND auction_house.guild_id = $2 AND auction_house.item_id = $3;
    """
    recreate_if_not_found = """
    INSERT INTO user_inv (owner_id, guild_id, item_id, amount_owned)
    VALUES ($1, $2, $3, $4)
    ON CONFLICT (owner_id, item_id) DO UPDATE
    SET amount_owned = user_inv.amount_owned + $4;
    """
    delete_from_ah = """
    DELETE FROM auction_house
    WHERE id = $1 AND user_id = $2 AND guild_id = $3;
    """

    async with pool.acquire() as conn:
        idx = await conn.fetchval(get_name_from_id, item_name, guild_id)
        rows = await conn.fetchrow(get_item_info, user_id, guild_id, item_id or idx)
        if rows is None:
            return "Item not found"
        records = dict(rows)
        general_item_id = records["item_id"]
        if idx is not None:
            general_item_id = idx
        if user_id != records["user_id"]:
            async with conn.transaction():
                await conn.execute(
                    recreate_if_not_found,
                    user_id,
                    guild_id,
                    general_item_id,
                    records["amount_listed"],
                )
                await conn.execute(delete_from_ah, records["id"], user_id, guild_id)
                return "Successfully deleted your listing"
        else:
            return "You aren't the owner!"


async def add_more_to_auction(
    guild_id: int,
    user_id: int,
    pool: asyncpg.Pool,
    amount_requested: int,
    item_name: Optional[str] = None,
    item_id: Optional[int] = None,
) -> str:
    get_name_from_id = """
    SELECT id FROM eco_item
    WHERE name = $1 AND guild_id = $2;
    """

    get_item_from_inv = """
    SELECT user_inv.amount_owned, user_inv.item_id, auction_house.amount_listed, auction_house.user_id
    FROM auction_house
    INNER JOIN user_inv ON user_inv.item_id = auction_house.item_id AND user_inv.owner_id = auction_house.user_id
    WHERE auction_house.user_id = $1 AND auction_house.guild_id = $2 AND auction_house.item_id = $3;
    """
    update_auction_amount = """
    UPDATE auction_house
    SET amount_listed = $4
    WHERE user_id = $1 AND guild_id = $2 AND item_id = $3;
    """
    subtract_from_inv = """
    UPDATE user_inv
    SET amount_owned = amount_owned - $4
    WHERE owner_id = $1 AND guild_id = $2 AND item_id = $3;
    """
    async with pool.acquire() as conn:
        idx = item_id
        # This is sus
        if item_id is None:
            id_val = await conn.fetchval(get_name_from_id, item_name, guild_id)
            if id_val is not None:
                idx = id_val

        get_info = await conn.fetchrow(get_item_from_inv, user_id, guild_id, idx)
        if get_info is None:
            return "Item not found"

        records = dict(get_info)

        if amount_requested > records["amount_owned"]:
            return "You dont have enough"

        if user_id != records["user_id"]:
            async with conn.transaction():
                await conn.execute(
                    update_auction_amount, user_id, guild_id, idx, amount_requested
                )
                await conn.execute(
                    subtract_from_inv, user_id, guild_id, idx, amount_requested
                )
                return "Successfully added more"
        else:
            return "You don't own this item"


async def obtain_item_info(
    guild_id: int, name: str, pool: asyncpg.Pool
) -> Union[Dict[str, Any], List[Dict[str, Any]], None]:
    sql = """
    SELECT eco_item.name, eco_item.description, auction_house.user_id, auction_house.amount_listed, auction_house.listed_price, auction_house.listed_at
    FROM auction_house
    INNER JOIN eco_item ON eco_item.name = $2
    WHERE auction_house.guild_id = $1;
    """
    async with pool.acquire() as conn:
        res = await conn.fetchrow(sql, guild_id, name.lower())
        if res is None:
            query = """
                SELECT eco_item.name
                FROM auction_house
                INNER JOIN eco_item ON eco_item.name % $2
                WHERE auction_house.guild_id=$1
                ORDER BY similarity(eco_item.name, $2) DESC
                LIMIT 5;
            """
            new_res = await conn.fetch(query, guild_id, name.lower())
            if new_res is None or len(new_res) == 0:
                return None

            return [dict(row) for row in new_res]

        return dict(res)
