-- Add migration script here
-- FIXME In order to make postgres to auto assign the database user to the table users being used
-- CREATE FUNCTION force_table_owner()
-- RETURNS event_trigger
-- LANGUAGE plpgsql
-- AS $$
-- BEGIN
--     EXECUTE format(
--         'ALTER TABLE %I.%I OWNER TO %I',
--         TG_TABLE_SCHEMA, TG_TABLE_NAME,
--         (SELECT datdba::regrole FROM pg_database WHERE datname = current_database())
--     );
-- END;
-- $$;
-- CREATE EVENT TRIGGER enforce_owner ON ddl_command_end WHEN TAG IN ('CREATE TABLE') EXECUTE FUNCTION force_table_owner();

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT NOT NULL UNIQUE,
    email TEXT NOT NULL UNIQUE,
    phone TEXT NOT NULL UNIQUE,
    google TEXT NULL UNIQUE,
    created_at INT,
    last_login INT
);
