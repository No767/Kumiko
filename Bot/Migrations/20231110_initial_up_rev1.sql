CREATE TABLE IF NOT EXISTS guild (
    id BIGINT PRIMARY KEY,
    prefix VARCHAR(255)[3],
    logs BOOLEAN DEFAULT TRUE,
    local_economy BOOLEAN DEFAULT FALSE,
    redirects BOOLEAN DEFAULT TRUE,
    pins BOOLEAN DEFAULT TRUE
);

CREATE TABLE IF NOT EXISTS logging_config (
    id SERIAL PRIMARY KEY,
    guild_id BIGINT REFERENCES guild (id) ON DELETE CASCADE ON UPDATE NO ACTION,
    mod BOOLEAN DEFAULT TRUE,
    eco BOOLEAN DEFAULT FALSE,
    redirects BOOLEAN DEFAULT FALSE
);

CREATE TABLE IF NOT EXISTS blacklist (
    id BIGINT PRIMARY KEY,
    blacklist_status BOOLEAN DEFAULT FALSE
);

CREATE INDEX IF NOT EXISTS logging_config_channel_id_uniq_idx ON logging_config (channel_id);
CREATE UNIQUE INDEX IF NOT EXISTS logging_config_guild_id_uniq_idx ON logging_config (guild_id);