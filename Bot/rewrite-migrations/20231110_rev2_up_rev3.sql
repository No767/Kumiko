CREATE TABLE IF NOT EXISTS pride_profiles (
    id BIGINT PRIMARY KEY,
    name VARCHAR(50),
    pronouns VARCHAR(50),
    gender_identity VARCHAR(50),
    sexual_orientation VARCHAR(50),
    romantic_orientation VARCHAR(50),
    views INT DEFAULT 0
);

-- Trigram indexes for GIN indexes to work properly
CREATE INDEX IF NOT EXISTS pride_profiles_name_idx ON pride_profiles (name);
CREATE INDEX IF NOT EXISTS pride_profiles_name_trgm_idx ON pride_profiles USING GIN (name gin_trgm_ops);
CREATE INDEX IF NOT EXISTS pride_profiles_name_lower_idx ON pride_profiles (LOWER(name));

CREATE TABLE IF NOT EXISTS timers (
    id SERIAL PRIMARY KEY,
    expires TIMESTAMP,
    created TIMESTAMP DEFAULT (now() at time zone 'utc'),
    event TEXT,
    timezone TEXT NOT NULL DEFAULT 'UTC',
    extra JSONB DEFAULT ('{}'::jsonb)
);

CREATE INDEX IF NOT EXISTS timers_expires_idx ON timers (expires);

CREATE TABLE IF NOT EXISTS user_settings (
    id BIGINT PRIMARY KEY, -- The discord user ID
    timezone TEXT -- The user's timezone
);