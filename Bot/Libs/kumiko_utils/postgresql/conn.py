from typing import List, Literal

from tortoise import BaseDBAsyncClient, Tortoise, connections


async def connectPostgres(uri: str, models: List[str]) -> Literal[True]:
    """Makes the connection to the PostgreSQL server

    Args:
        uri (str): Connection URI
        models (List[str]): List of models to use

    Returns:
        Literal[True]: Returns True if successful
    """
    await Tortoise.init(db_url=uri, modules={"models": models})
    conn: BaseDBAsyncClient = connections.get("default")
    await conn.create_connection(with_db=True)
    return True
