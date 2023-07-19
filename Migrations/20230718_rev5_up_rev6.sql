ALTER TABLE job ADD COLUMN creator_id BIGINT;
ALTER TABLE job RENAME COLUMN owner_id TO worker_id;
ALTER TABLE job_lookup ADD COLUMN worker_id BIGINT;
ALTER TABLE job_lookup RENAME COLUMN owner_id TO creator_id;

DROP INDEX IF EXISTS job_owner_id_uniq_idx;
CREATE UNIQUE INDEX IF NOT EXISTS job_worker_id_uniq_idx ON job (LOWER(name), worker_id);
CREATE UNIQUE INDEX IF NOT EXISTS job_lookup_worker_id_uniq_idx ON job_lookup (LOWER(name), worker_id);
CREATE UNIQUE INDEX IF NOT EXISTS job_creator_id_uniq_idx ON job (LOWER(name), creator_id);