-- Add migration script here
ALTER TABLE users ALTER created_at TYPE int8;
ALTER TABLE users ALTER last_login TYPE int8;