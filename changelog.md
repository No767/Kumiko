# ✨ Kumiko v0.5.0 ✨


## ✨ TD;LR

- Migrate from SQLAlchemy ORM to Tortoise ORM
- Kumiko's custom caching library (w/ coredis)

## 🛠️ Changes
- Subclass Kumiko instead of creating the instance from `discord.Bot`
- Replace SQLAlchemy with Tortoise ORM
- Cache GWS Profiles, invs, etc
- Optimize GWS pull commands
- Update Python constraints (>=3.8,<4.0)
- Upgrade PostgreSQL Dockerfile versions to 15
- Include Rust (rustc and cargo) when building orjson and ormsgpack 
- Use Ormsgpack for MessagePack serialization
- Update docs (as per usual)
- Switch to using Python 3.11.0 for Dockerfiles, and officially support Python 3.11.0 for Kumiko

## ✨ Additions

- Kumiko's custom caching library (w/ coredis)
- New delete interface for GWS inv
- MessagePack serialization for Redis

## ➖ Removals
- SQLAlchemy ORM code