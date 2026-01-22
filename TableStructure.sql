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

curl -X POST http://127.0.0.1:5555/users \
     -H "Content-Type: application/json" \
     -d '{
           "username": "john_doe",
           "email": "john@example.com",
           "password_hash": "hashed_password_here"
         }'
