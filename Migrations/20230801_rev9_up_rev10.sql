CREATE TABLE IF NOT EXISTS user_item_relations (
    id SERIAL PRIMARY KEY,
    item_id INT FOREIGN KEY REFERENCES eco_item (id) ON DELETE CASCADE ON UPDATE NO ACTION,
    user_id BIGINT REFERENCES eco_user (id) ON DELETE CASCADE ON UPDATE NO ACTION
);

CREATE INDEX IF NOT EXISTS user_item_relations_item_idx ON user_item_relations (item_id);
CREATE INDEX IF NOT EXISTS user_item_relations_user_idx ON user_item_relations (user_id);