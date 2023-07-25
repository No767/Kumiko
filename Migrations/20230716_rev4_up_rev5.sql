CREATE TABLE IF NOT EXISTS job (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255),
    description TEXT,
    required_rank INTEGER DEFAULT 0,
    pay_amount INTEGER DEFAULT 15, -- Same thing as most US min wages
    created_at TIMESTAMP DEFAULT (NOW() AT TIME ZONE 'utc'),
    guild_id BIGINT REFERENCES guild (id) ON DELETE CASCADE ON UPDATE NO ACTION,
    owner_id BIGINT REFERENCES eco_user (id) ON DELETE CASCADE ON UPDATE NO ACTION
);

CREATE TABLE IF NOT EXISTS job_lookup (
    id SERIAL PRIMARY KEY,
    name TEXT,
    guild_id BIGINT,
    owner_id BIGINT,
    listed BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT (NOW() AT TIME ZONE 'utc'),
    job_id INTEGER REFERENCES job (id) ON DELETE CASCADE ON UPDATE NO ACTION
);

CREATE INDEX IF NOT EXISTS job_name_idx ON job (name);
CREATE INDEX IF NOT EXISTS job_name_trgm_idx ON job USING GIN (name gin_trgm_ops);
CREATE INDEX IF NOT EXISTS job_name_lower_idx ON job (LOWER(name));
CREATE UNIQUE INDEX IF NOT EXISTS job_uniq_idx ON job (LOWER(name), guild_id);
CREATE UNIQUE INDEX IF NOT EXISTS job_owner_id_uniq_idx ON job (LOWER(name), owner_id);

CREATE INDEX IF NOT EXISTS job_lookup_name_idx ON job_lookup (name);
CREATE INDEX IF NOT EXISTS job_lookup_guild_id_idx ON job_lookup (guild_id);
CREATE INDEX IF NOT EXISTS job_lookup_name_trgm_idx ON job_lookup USING GIN (name gin_trgm_ops);
CREATE INDEX IF NOT EXISTS job_lookup_name_lower_idx ON job_lookup (LOWER(name));
CREATE UNIQUE INDEX IF NOT EXISTS job_lookup_uniq_idx ON job_lookup (LOWER(name), guild_id);