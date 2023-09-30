-- ALTER TABLE user_settings ADD COLUMN antiping BOOLEAN DEFAULT FALSE;
ALTER TABLE user_settings ADD COLUMN antiping_embed JSONB DEFAULT ('{}'::jsonb);

CREATE TABLE IF NOT EXISTS antiping_sessions (
    id SERIAL PRIMARY KEY,
    user_id BIGINT,
    session_enabled BOOLEAN DEFAULT FALSE,
    UNIQUE (user_id)
);

CREATE INDEX IF NOT EXISTS antiping_sessions_user_id_idx ON antiping_sessions (user_id);