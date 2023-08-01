CREATE TABLE IF NOT EXISTS user_item_relations (
    id SERIAL PRIMARY KEY,
    item_id INT,
    user_id BIGINT REFERENCES eco_user (id) ON DELETE CASCADE ON UPDATE NO ACTION,
    FOREIGN KEY (item_id) REFERENCES eco_item (id) ON DELETE CASCADE ON UPDATE NO ACTION
);

CREATE INDEX IF NOT EXISTS user_item_relations_item_idx ON user_item_relations (item_id);
CREATE INDEX IF NOT EXISTS user_item_relations_user_idx ON user_item_relations (user_id);