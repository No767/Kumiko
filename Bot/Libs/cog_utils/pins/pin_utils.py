from typing import Dict, List, Union

import asyncpg
from discord.ext.commands import Context


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
    query = """
    SELECT pin.name, pin.content, pin.created_at, pin.author_id, pin_lookup.aliases
    FROM pin_lookup
    INNER JOIN pin ON pin.id = pin_lookup.pin_id
    WHERE pin_lookup.guild_id=$1 AND LOWER(pin_lookup.name)=$2 OR LOWER(pin_lookup.name) = ANY(aliases);
    """
    async with pool.acquire() as conn:
        res = await conn.fetchrow(query, id, pin_name)
        if res is None:
            return None
        return dict(res)


async def createPin(ctx: Context, pool: asyncpg.Pool, name: str, content: str) -> None:
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
                ctx.author.id,
                ctx.guild.id,  # type: ignore
                name,
                content,
            )
        except asyncpg.UniqueViolationError:
            await tr.rollback()
            await ctx.send("The pin (`{name}`) already exists.")
        except Exception:
            await tr.rollback()
            await ctx.send("Could not create pin")
        else:
            await tr.commit()
            await ctx.send(f"Pin `{name}` successfully created")


async def editPin(
    guild_id: int, author_id: int, pool: asyncpg.Pool, name: str, content: str
) -> str:
    query = """
    UPDATE pin
    SET content = $1
    WHERE guild_id = $3 AND LOWER(pin.name) = $2 AND author_id = $4;
    """
    async with pool.acquire() as conn:
        status = await conn.execute(
            query, content, name, guild_id, author_id  # type: ignore
        )
        return status
