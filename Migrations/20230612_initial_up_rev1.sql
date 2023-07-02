-- Initial Migrations
-- Created while I am in Saijo, Ehime

CREATE TABLE IF NOT EXISTS guild (
    id BIGINT PRIMARY KEY,
    prefix VARCHAR(255) NOT NULL,
    logs BOOLEAN DEFAULT FALSE,
    birthday BOOLEAN DEFAULT FALSE,
    local_economy BOOLEAN DEFAULT FALSE
);

CREATE TABLE IF NOT EXISTS eco_user (
    id BIGINT PRIMARY KEY,
    rank INT DEFAULT 0,
    petals INT DEFAULT 0,
    date_joined timestamp WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL
);

CREATE TABLE IF NOT EXISTS eco_item (
    id SERIAL PRIMARY KEY,
    user_id BIGINT,
    name VARCHAR(255),
    description TEXT,
    price INT DEFAULT 0,
    amount INT DEFAULT 0,
    CONSTRAINT fk_user FOREIGN KEY (user_id) REFERENCES eco_user (id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS marketplace (
    id SERIAL PRIMARY KEY,
    guild_id BIGINT,
    name VARCHAR(255),
    description TEXT,
    date_created timestamp WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
    CONSTRAINT fk_guild FOREIGN KEY (guild_id) REFERENCES guild (id) ON DELETE CASCADE
);
