-- Add migration script here
CREATE TABLE contact_posts (
    id SERIAL PRIMARY KEY,
    name TEXT,
    email TEXT,
    message TEXT,
    created_at INT8
);
CREATE TABLE contacts (
    id SERIAL PRIMARY KEY NOT NULL,
    email TEXT,
    phone TEXT,
    address TEXT,
    facebook TEXT NULL,
    twitter TEXT NULL,
    instagram TEXT NULL,
    dribble TEXT NULL,
    behance TEXT NULL
);