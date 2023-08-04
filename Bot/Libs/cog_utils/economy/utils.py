import asyncpg


async def refund_item(
    guild_id: int, user_id: int, item_id: int, amount: int, pool: asyncpg.Pool
):
    sql = """
    SELECT eco_item.name, eco_item.price, user_inv.owner_id, user_inv.amount_owned, user_inv.item_id
    FROM user_inv
    INNER JOIN eco_item ON eco_item.id = user_inv.item_id
    WHERE user_inv.owner_id =  $1 AND user_inv.guild_id = $2 AND eco_item.id = $3;
    """
    subtract_owned_items = """
    UPDATE user_inv
    SET amount_owned = amount_owned - $1
    WHERE owner_id = $2 AND guild_id = $3 AND item_id = $4;
    """
    add_back_items_to_stock = """
    UPDATE eco_item
    SET amount = amount + $1
    WHERE id = $2;
    """
    add_back_price = """
    UPDATE eco_user
    SET petals = petals + $1
    WHERE id = $2;
    """
    async with pool.acquire() as conn:
        rows = await conn.fetchrow(sql, user_id, guild_id, item_id)
        if rows is None:
            # idk probably return str status
            return "User does not own this item!"
        records = dict(rows)
        refund_price = ((records["price"] * amount) / 4) * 3
        if amount > records["amount_owned"]:
            return "User does not own that many items!"
        async with conn.transaction():
            await conn.execute(
                subtract_owned_items,
                amount,
                user_id,
                guild_id,
                records["item_id"],
            )
            await conn.execute(add_back_items_to_stock, amount, records["item_id"])
            await conn.execute(add_back_price, refund_price, user_id)
        return "Successfully refunded your item!"
