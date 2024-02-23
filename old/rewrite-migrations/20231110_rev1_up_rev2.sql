CREATE TABLE IF NOT EXISTS eco_user (
    id BIGINT PRIMARY KEY,
    rank INT DEFAULT 0,
    petals INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT (NOW() AT TIME ZONE 'utc')
);

CREATE TABLE IF NOT EXISTS eco_item (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255),
    description TEXT,
    price INT DEFAULT 0 CHECK (price > 0),
    amount INT DEFAULT 1 CHECK (amount >= 0),
    restock_amount INT DEFAULT 0 CHECK (restock_amount >= 1),
    created_at TIMESTAMP DEFAULT (NOW() AT TIME ZONE 'utc'),
    guild_id BIGINT REFERENCES guild (id),
    producer_id BIGINT REFERENCES eco_user (id),
    owner_id BIGINT REFERENCES eco_user (id) ON DELETE CASCADE ON UPDATE NO ACTION,
    UNIQUE (producer_id, owner_id)
);

CREATE INDEX IF NOT EXISTS eco_item_name_idx ON eco_item (name);
CREATE INDEX IF NOT EXISTS eco_item_name_trgm_idx ON eco_item USING GIN (name gin_trgm_ops);
CREATE INDEX IF NOT EXISTS eco_item_name_lower_idx ON eco_item (LOWER(name));
CREATE UNIQUE INDEX IF NOT EXISTS eco_item_uniq_idx ON eco_item (LOWER(name), guild_id);
CREATE INDEX IF NOT EXISTS eco_item_producer_id_idx ON eco_item (producer_id);


CREATE TABLE IF NOT EXISTS user_inv (
    id SERIAL PRIMARY KEY,
    owner_id BIGINT,
    guild_id BIGINT,
    amount_owned INT DEFAULT 0,
    item_id INT,
    UNIQUE (owner_id, item_id),
    FOREIGN KEY (item_id) REFERENCES eco_item (id) ON DELETE CASCADE ON UPDATE NO ACTION
);

CREATE INDEX IF NOT EXISTS user_inv_owner_idx ON user_inv (owner_id);
CREATE INDEX IF NOT EXISTS user_inv_guild_idx ON user_inv (guild_id);
CREATE INDEX IF NOT EXISTS user_inv_item_idx ON user_inv (item_id);

CREATE TABLE IF NOT EXISTS job (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255),
    description TEXT,
    required_rank INTEGER DEFAULT 0,
    pay_amount INTEGER DEFAULT 15, -- Same thing as most US min wages
    created_at TIMESTAMP DEFAULT (NOW() AT TIME ZONE 'utc'),
    guild_id BIGINT REFERENCES guild (id) ON DELETE CASCADE ON UPDATE NO ACTION,
    worker_id BIGINT REFERENCES eco_user (id) ON DELETE CASCADE ON UPDATE NO ACTION,
    creator_id BIGINT REFERENCES eco_user (id) ON DELETE CASCADE ON UPDATE NO ACTION
);

CREATE INDEX IF NOT EXISTS job_name_idx ON job (name);
CREATE INDEX IF NOT EXISTS job_name_trgm_idx ON job USING GIN (name gin_trgm_ops);
CREATE INDEX IF NOT EXISTS job_name_lower_idx ON job (LOWER(name));
CREATE UNIQUE INDEX IF NOT EXISTS job_uniq_idx ON job (LOWER(name), guild_id);
CREATE UNIQUE INDEX IF NOT EXISTS job_worker_id_uniq_idx ON job (LOWER(name), worker_id);
CREATE UNIQUE INDEX IF NOT EXISTS job_creator_id_uniq_idx ON job (LOWER(name), creator_id);

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

CREATE TABLE IF NOT EXISTS auction_house (
    id SERIAL PRIMARY KEY,
    item_id INT,
    user_id BIGINT,
    guild_id BIGINT REFERENCES guild (id),
    amount_listed INT,
    listed_price INT,
    listed_at TIMESTAMP DEFAULT (NOW() AT TIME ZONE 'utc'),
    UNIQUE (item_id, user_id),
    FOREIGN KEY (item_id) REFERENCES eco_item (id) ON DELETE CASCADE ON UPDATE NO ACTION,
    FOREIGN KEY (user_id) REFERENCES eco_user (id) ON DELETE CASCADE ON UPDATE NO ACTION
);

CREATE INDEX IF NOT EXISTS auction_house_user_idx ON auction_house (user_id);
CREATE INDEX IF NOT EXISTS auction_house_item_idx ON auction_house (item_id);