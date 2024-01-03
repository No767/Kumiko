DROP TABLE IF EXISTS blacklist;

CREATE TABLE IF NOT EXISTS blacklist (
    id SERIAL PRIMARY KEY,
    entity_id BIGINT NOT NULL,
    entity_type INT,
    status BOOLEAN DEFAULT TRUE
);

CREATE INDEX IF NOT EXISTS blacklist_entity_id_idx ON blacklist (entity_id);
