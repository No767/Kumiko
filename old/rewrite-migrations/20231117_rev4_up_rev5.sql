ALTER TABLE logging_config DROP COLUMN IF EXISTS channel_id;
ALTER TABLE logging_config DROP COLUMN IF EXISTS webhook_id;

CREATE TABLE IF NOT EXISTS logging_webhooks (
    id BIGINT PRIMARY KEY REFERENCES guild (id) ON DELETE CASCADE ON UPDATE NO ACTION,
    channel_id BIGINT,
    broadcast_url TEXT,
    locked BOOLEAN DEFAULT FALSE
);