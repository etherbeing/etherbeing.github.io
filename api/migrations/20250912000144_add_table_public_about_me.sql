-- Add migration script here
CREATE TABLE public_about_me (
    name TEXT,
    pitch TEXT, 
    slogan TEXT, 
    photo TEXT,
    content TEXT, 
    cv_file TEXT 
);
-- Populates the fields with empty values as this is a singleton model
insert into public_about_me VALUES ('', '', '', '', '', '');