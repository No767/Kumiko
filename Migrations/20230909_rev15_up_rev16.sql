CREATE TABLE IF NOT EXISTS blacklist (
    id BIGINT PRIMARY KEY,
    blacklist_status BOOLEAN DEFAULT FALSE
);