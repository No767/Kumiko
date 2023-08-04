import asyncpg


async def create_auction(guild_id: int, user_id: int, item_id: int, pool: asyncpg.Pool):
    take_from_user_inv = """
    """
