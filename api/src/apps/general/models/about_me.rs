use serde::{Deserialize, Serialize};
use sqlx;
use utoipa::ToSchema;

#[derive(Serialize, Deserialize, ToSchema, Debug, sqlx::FromRow)]
pub struct AboutMe {
    name: String,
    pitch: String,  // used at the banner in the home page at the beggining
    slogan: String, // In the about me section the first text it shows is this (in h2 probably)
    photo: String,
    content: String, // Rich Text content
    cv_file: String,
}
