-- Add migration script here
CREATE TABLE client (
    id BIGSERIAL PRIMARY KEY,
    name TEXT,
    role TEXT NULL,
    avatar TEXT NULL,
    logo TEXT
);
CREATE TYPE PortfolioType as ENUM ('SimpleImage', 'SimpleVideo', 'Detailed');
CREATE TABLE portfolio_item (
    id BIGSERIAL PRIMARY KEY,
    title TEXT,
    subtitle TEXT,
    image TEXT,
    project_date DATE,
    role TEXT,
    client BIGINT NOT NULL REFERENCES client(id) ON DELETE RESTRICT,
    public_url TEXT NULL,
    description  TEXT,
    youtube_url TEXT NULL,
    portfolio_type PortfolioType NOT NULL
);