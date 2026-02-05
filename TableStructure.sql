CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    email VARCHAR(120) NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

GRANT SELECT, INSERT, UPDATE, DELETE ON users TO myapp_user;
GRANT USAGE, SELECT, UPDATE ON SEQUENCE users_id_seq TO myapp_user;

ALTER TABLE users OWNER TO myapp_user;
ALTER SEQUENCE users_id_seq OWNER TO myapp_user;


curl -X POST http://127.0.0.1:5555/default/users \
     -H "Content-Type: application/json" \
     -d '{
           "username": "john_doe",
           "email": "john@example.com",
           "password_hash": "hashed_password_here"
         }'

CREATE TABLE tree_nodes (
    node_id SERIAL PRIMARY KEY,
    parent_id INT REFERENCES tree_nodes(node_id) ON DELETE CASCADE
);

CREATE TABLE node_metadata (
    metadata_id SERIAL PRIMARY KEY,
    node_id INT NOT NULL REFERENCES tree_nodes(node_id) ON DELETE CASCADE,
    key_name TEXT NOT NULL,  -- e.g. 'name', 'created_at', 'priority'
    
    -- Possible PostgreSQL data types
    value_text TEXT,
    value_int INT,
    value_numeric NUMERIC,
    value_boolean BOOLEAN,
    value_date DATE,
    value_timestamp TIMESTAMP,
    value_json JSONB,
    value_uuid UUID,
    value_bytea BYTEA,
    
    -- Ensure only one value column is filled per row
    CONSTRAINT one_value CHECK (
        (value_text IS NOT NULL)::int +
        (value_int IS NOT NULL)::int +
        (value_numeric IS NOT NULL)::int +
        (value_boolean IS NOT NULL)::int +
        (value_date IS NOT NULL)::int +
        (value_timestamp IS NOT NULL)::int +
        (value_json IS NOT NULL)::int +
        (value_uuid IS NOT NULL)::int +
        (value_bytea IS NOT NULL)::int = 1
    )
);

-- Insert root node
INSERT INTO tree_nodes (parent_id) VALUES (NULL);

-- Add metadata: name and created_at
INSERT INTO node_metadata (node_id, key_name, value_text)
VALUES (1, 'name', 'Root');

INSERT INTO node_metadata (node_id, key_name, value_timestamp)
VALUES (1, 'created_at', CURRENT_TIMESTAMP);

-- Insert child node
INSERT INTO tree_nodes (parent_id) VALUES (1);

-- Add metadata: name
INSERT INTO node_metadata (node_id, key_name, value_text)
VALUES (2, 'name', 'Child A');


curl -X POST  http://127.0.0.1:5555/default/nodes \
  -H "Content-Type: application/json" \
  -d '{"parent_id": 1}'

curl  http://127.0.0.1:5555/default/nodes/2

curl -X PUT  http://127.0.0.1:5555/default/nodes/2 \
  -H "Content-Type: application/json" \
  -d '{"parent_id": 5}'

curl -X DELETE  http://127.0.0.1:5555/default/nodes/2

curl -X POST  http://127.0.0.1:5555/default/nodes/1/metadata \
  -H "Content-Type: application/json" \
  -d '{
    "key_name": "title",
    "value": "Root Node"
  }'

-d '{"key_name":"active","value":true}'
-d '{"key_name":"priority","value":10}'
-d '{"key_name":"config","value":{"x":1,"y":2}}'

curl -X PUT  http://127.0.0.1:5555/default/metadata/3 \
  -H "Content-Type: application/json" \
  -d '{"value": "Updated Title"}'
curl -X DELETE  http://127.0.0.1:5555/default/metadata/3

GRANT USAGE, SELECT, UPDATE ON SEQUENCE tree_nodes_node_id_seq TO system;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO system;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO system;

curl -X POST  http://127.0.0.1:5555/default/nodes -H "Content-Type: application/json" -d '{}'
curl -X POST  http://127.0.0.1:5555/default/nodes \
  -H "Content-Type: application/json" \
  -d '{"parent_id": 1}'
curl -X POST  http://127.0.0.1:5555/default/nodes/1/metadata \
  -H "Content-Type: application/json" \
  -d '{"key_name":"name","value":"Root"}'
curl  http://127.0.0.1:5555/default/nodes/1
curl -X PUT  http://127.0.0.1:5555/default/metadata/1 \
  -H "Content-Type: application/json" \
  -d '{"value":"Renamed Root"}'
curl -X DELETE  http://127.0.0.1:5555/default/metadata/1

curl -s -X POST http://127.0.0.1:5555/default/sql \
  -H "Content-Type: application/json" \
  -d '{"query":"SELECT * from users;"}'

  curl -s -X POST http://127.0.0.1:5555/default/sql \
  -H "Content-Type: application/json" \
  -d '{"query":"SELECT * from tree_nodes;"}'

  curl -s -X POST http://127.0.0.1:5555/default/sql \
  -H "Content-Type: application/json" \
  -d '{"query":"SELECT * from node_metadata;"}'