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