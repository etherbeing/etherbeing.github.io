-- Add migration script here
CREATE TABLE messages (
    id SERIAL PRIMARY KEY,
    content TEXT NOT NULL
)