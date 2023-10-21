ALTER TABLE guild DROP COLUMN birthday;
ALTER TABLE guild DROP COLUMN local_economy_name;

ALTER TABLE logging_config DROP COLUMN member_events;
ALTER TABLE logging_config RENAME COLUMN mod_events TO mod;
ALTER TABLE logging_config RENAME COLUMN eco_events TO eco;
ALTER TABLE logging_config ADD COLUMN redirects BOOLEAN DEFAULT FALSE;