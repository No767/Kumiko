-- Techincially speaking up, the base eco_user tables makes the economy system global
-- By setting up an 1-n relationship, we basically make it local instead
-- More expensive? Yes. Worth it? Maybe

ALTER TABLE eco_item DROP CONSTRAINT fk_user;
ALTER TABLE eco_item DROP COLUMN user_id;
ALTER TABLE eco_item ADD COLUMN producer_id BIGINT;
ALTER TABLE eco_item ADD COLUMN owner_id BIGINT REFERENCES eco_user (id) ON DELETE CASCADE ON UPDATE NO ACTION;
ALTER TABLE eco_item ADD COLUMN created_at TIMESTAMP DEFAULT (NOW() AT TIME ZONE 'utc');
ALTER TABLE eco_item_lookup DROP COLUMN created_at;
ALTER TABLE eco_item_lookup ADD COLUMN producer_id BIGINT;

CREATE INDEX IF NOT EXISTS eco_item_producer_id_idx ON eco_item (producer_id);
CREATE INDEX IF NOT EXISTS eco_item_lookup_producer_id_idx ON eco_item_lookup (producer_id);

-- essentially we have an m-m relationship now
-- what have i done i have sinned
CREATE TABLE IF NOT EXISTS job_output (
    id SERIAL PRIMARY KEY,
    worker_id BIGINT,
    item_id INT REFERENCES eco_item (id) ON DELETE CASCADE ON UPDATE NO ACTION,
    job_id INT REFERENCES job (id) ON DELETE CASCADE ON UPDATE NO ACTION
);

CREATE INDEX IF NOT EXISTS job_output_item_id_idx ON job_output (item_id);
CREATE INDEX IF NOT EXISTS job_output_job_id_idx ON job_output (job_id);


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