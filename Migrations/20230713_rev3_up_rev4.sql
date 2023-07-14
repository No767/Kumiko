-- Pins are basically like tags. but rebranded

CREATE TABLE IF NOT EXISTS pin (
    id SERIAL PRIMARY KEY,
    author_id BIGINT,
    name VARCHAR(255),
    aliases TEXT[],
    content TEXT,
    created_at timestamp WITHOUT TIME ZONE DEFAULT (NOW() AT TIME ZONE 'utc'),
    guild_id BIGINT REFERENCES guild (id) ON DELETE CASCADE ON UPDATE NO ACTION
);

CREATE TABLE IF NOT EXISTS pin_lookup (
    id SERIAL PRIMARY KEY,
    name TEXT,
    guild_id BIGINT,
    owner_id BIGINT,
    created_at TIMESTAMP DEFAULT (now() AT TIME ZONE 'utc'),
    pin_id INTEGER REFERENCES pin (id) ON DELETE CASCADE ON UPDATE NO ACTION
);

CREATE INDEX IF NOT EXISTS pin_name_idx ON pin (name);
CREATE INDEX IF NOT EXISTS pin_name_trgm_idx ON pin USING GIN (name gin_trgm_ops);
CREATE INDEX IF NOT EXISTS pin_name_lower_idx ON pin (LOWER(name));
CREATE UNIQUE INDEX IF NOT EXISTS pin_uniq_idx ON pin (LOWER(name), guild_id);

CREATE INDEX IF NOT EXISTS pin_lookup_name_idx ON pin_lookup (name);
CREATE INDEX IF NOT EXISTS pin_lookup_location_id_idx ON pin_lookup (guild_id);
CREATE INDEX IF NOT EXISTS pin_lookup_name_trgm_idx ON pin_lookup USING GIN (name gin_trgm_ops);
CREATE INDEX IF NOT EXISTS pin_lookup_name_lower_idx ON pin_lookup (LOWER(name));
CREATE UNIQUE INDEX IF NOT EXISTS pin_lookup_uniq_idx ON pin_lookup (LOWER(name), guild_id);