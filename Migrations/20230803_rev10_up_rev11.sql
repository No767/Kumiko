CREATE TABLE IF NOT EXISTS auction_house (
    id SERIAL PRIMARY KEY,
    item_id INT,
    user_id BIGINT REFERENCES eco_user (id) ON DELETE CASCADE ON UPDATE NO ACTION,
    guild_id BIGINT,
    amount_listed INT,
    listed_at TIMESTAMP DEFAULT (NOW() AT TIME ZONE 'utc'),
    FOREIGN KEY (item_id) REFERENCES eco_item (id) ON DELETE CASCADE ON UPDATE NO ACTION
);

CREATE TABLE IF NOT EXISTS ah_user_bridge (
    id SERIAL PRIMARY KEY,
    user_id BIGINT REFERENCES eco_user (id) ON DELETE CASCADE ON UPDATE NO ACTION,
    ah_item_id INT,
    FOREIGN KEY (ah_item_id) REFERENCES auction_house (id) ON DELETE CASCADE ON UPDATE NO ACTION
);

CREATE INDEX IF NOT EXISTS auction_house_listed_at ON auction_house (listed_at);
CREATE INDEX IF NOT EXISTS ah_user_bridge_user_idx ON ah_user_bridge (user_id);
CREATE INDEX IF NOT EXISTS ah_user_bridge_ah_item_idx ON ah_user_bridge (ah_item_id);
