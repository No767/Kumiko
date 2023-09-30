-- This table and following system comes from RoboDanny. 
-- I don't really see a need to recreate my own system bc I'm pretty much running short on time anyways
-- Originally I was going to use Sinbad's scheduler impl but that is for sqlite and it would be hard to translate it for asyncpg / postgres
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
