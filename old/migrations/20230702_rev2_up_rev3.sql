ALTER TABLE guild ADD COLUMN local_economy_name VARCHAR(255) DEFAULT 'Server Economy';

CREATE TABLE IF NOT EXISTS logging_config (
    id SERIAL PRIMARY KEY,
    channel_id BIGINT,
    member_events BOOLEAN DEFAULT TRUE,
    mod_events BOOLEAN DEFAULT TRUE,
    eco_events BOOLEAN DEFAULT FALSE,
    guild_id BIGINT UNIQUE REFERENCES guild (id) ON DELETE CASCADE ON UPDATE NO ACTION
);