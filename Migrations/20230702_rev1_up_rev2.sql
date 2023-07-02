ALTER TABLE eco_user ALTER COLUMN created_at SET DEFAULT (NOW() AT TIME ZONE 'utc');
ALTER TABLE marketplace ALTER COLUMN created_at SET DEFAULT (NOW() AT TIME ZONE 'utc');

ALTER TABLE guild ALTER COLUMN prefix SET DATA TYPE VARCHAR(255)[];

CREATE TABLE IF NOT EXISTS eco_item_lookup (
    id SERIAL PRIMARY KEY,
    name TEXT,
    guild_id BIGINT,
    owner_id BIGINT,
    created_at TIMESTAMP DEFAULT (now() AT TIME ZONE 'utc'),
    item_id INTEGER REFERENCES eco_item (id) ON DELETE CASCADE ON UPDATE NO ACTION
);

CREATE INDEX IF NOT EXISTS eco_item_name_idx ON eco_item (name);
CREATE INDEX IF NOT EXISTS eco_item_name_trgm_idx ON eco_item USING GIN (name gin_trgm_ops);
CREATE INDEX IF NOT EXISTS eco_item_name_lower_idx ON eco_item (LOWER(name));
CREATE UNIQUE INDEX IF NOT EXISTS eco_item_uniq_idx ON eco_item (LOWER(name), guild_id);

CREATE INDEX IF NOT EXISTS eco_item_lookup_name_idx ON eco_item_lookup (name);
CREATE INDEX IF NOT EXISTS eco_item_lookup_location_id_idx ON eco_item_lookup (guild_id);
CREATE INDEX IF NOT EXISTS eco_item_lookup_name_trgm_idx ON eco_item_lookup USING GIN (name gin_trgm_ops);
CREATE INDEX IF NOT EXISTS eco_item_lookup_name_lower_idx ON eco_item_lookup (LOWER(name));
CREATE UNIQUE INDEX IF NOT EXISTS eco_item_lookup_uniq_idx ON eco_item_lookup (LOWER(name), guild_id);