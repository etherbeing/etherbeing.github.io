-- Add migration script here
ALTER TABLE users DROP COLUMN phone;
ALTER TABLE users ADD COLUMN country int;