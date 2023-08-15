-- This migration is made to drop unused tables

DROP INDEX IF EXISTS ah_user_bridge_user_idx;
DROP INDEX IF EXISTS ah_user_bridge_ah_item_idx;
DROP TABLE IF EXISTS ah_user_bridge;

DROP INDEX IF EXISTS user_item_relations_item_idx;
DROP INDEX IF EXISTS user_item_relations_user_idx;
DROP TABLE IF EXISTS user_item_relations;

DROP INDEX IF EXISTS guild_eco_user_uniq_idx;
DROP INDEX IF EXISTS guild_eco_user_uniq_user_idx;
DROP TABLE IF EXISTS guild_eco_user;

DROP INDEX IF EXISTS job_output_item_id_idx;
DROP INDEX IF EXISTS job_output_job_id_idx;
DROP TABLE IF EXISTS job_output;