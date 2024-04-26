import asyncpg
import msgspec


async def init_codecs(conn: asyncpg.connection.Connection):
    def _encode_jsonb(value):
        return msgspec.json.encode(value)

    def _decode_jsonb(value):
        return msgspec.json.decode(value)

    await conn.set_type_codec(
        "jsonb",
        schema="pg_catalog",
        encoder=_encode_jsonb,
        decoder=_decode_jsonb,
        format="text",
    )
