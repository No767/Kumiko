-- Techincially speaking up, the base eco_user tables makes the economy system global
-- By setting up an 1-n relationship, we basically make it local instead
-- More expensive? Yes. Worth it? Maybe

CREATE TABLE IF NOT EXISTS guild_eco_user (
    id SERIAL PRIMARY KEY,
    user_id BIGINT,
    rank INT,
    petals INT,
    created_at TIMESTAMP DEFAULT (NOW() AT TIME ZONE 'utc'),
    guild_id BIGINT REFERENCES guild (id) ON DELETE CASCADE ON UPDATE NO ACTION
);

CREATE UNIQUE INDEX IF NOT EXISTS guild_eco_user_uniq_idx ON guild_eco_user (guild_id);
CREATE UNIQUE INDEX IF NOT EXISTS guild_eco_user_uniq_user_idx ON guild_eco_user (user_id);