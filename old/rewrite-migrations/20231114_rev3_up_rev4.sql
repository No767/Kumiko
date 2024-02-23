CREATE TABLE IF NOT EXISTS pins (
    id SERIAL PRIMARY KEY,
    name TEXT,
    content TEXT,
    owner_id BIGINT,
    uses INTEGER DEFAULT (0),
    guild_id BIGINT,
    created_at TIMESTAMP DEFAULT (now() at time zone 'utc')
);

CREATE INDEX IF NOT EXISTS pins_name_idx ON pins (name);
CREATE INDEX IF NOT EXISTS pins_guild_id_idx ON pins (guild_id);
CREATE INDEX IF NOT EXISTS pins_name_trgm_idx ON pins USING GIN (name gin_trgm_ops);
CREATE INDEX IF NOT EXISTS pins_name_lower_idx ON pins (LOWER(name));
CREATE UNIQUE INDEX IF NOT EXISTS pins_uniq_idx ON pins (LOWER(name), guild_id);

CREATE TABLE IF NOT EXISTS pin_lookup (
    id SERIAL PRIMARY KEY,
    name TEXT,
    guild_id BIGINT,
    owner_id BIGINT,
    created_at TIMESTAMP DEFAULT (now() at time zone 'utc'),
    pin_id INTEGER REFERENCES pins (id) ON DELETE CASCADE ON UPDATE NO ACTION
);

CREATE INDEX IF NOT EXISTS pin_lookup_name_idx ON pin_lookup (name);
CREATE INDEX IF NOT EXISTS pin_lookup_guild_id_idx ON pin_lookup (guild_id);
CREATE INDEX IF NOT EXISTS pin_lookup_name_trgm_idx ON pin_lookup USING GIN (name gin_trgm_ops);
CREATE INDEX IF NOT EXISTS pin_lookup_name_lower_idx ON pin_lookup (LOWER(name));
CREATE UNIQUE INDEX IF NOT EXISTS pin_lookup_uniq_idx ON pin_lookup (LOWER(name), guild_id);