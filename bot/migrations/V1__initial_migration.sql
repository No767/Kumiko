-- Revision Version: V1
-- Revises: V0
-- Creation Date: 2024-04-28 00:16:33.339328 UTC
-- Reason: initial_migration

CREATE TABLE IF NOT EXISTS guild_config (
    id BIGINT PRIMARY KEY,
    prefix TEXT[]
);