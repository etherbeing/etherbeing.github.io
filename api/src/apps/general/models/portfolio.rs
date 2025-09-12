use serde::{Deserialize, Serialize};
use sqlx::prelude::FromRow;
use utoipa::ToSchema;

use super::clients::{Client};

#[derive(ToSchema, Serialize, Debug, Deserialize)]
pub enum PortfolioType {
    SimpleImage, // Is just part of the image gallery not a page by itself
    SimpleVideo, // Is just part of the image gallery not a page by itself but it renders a video
    Detailed // Portfolio 2
}
#[derive(Debug, FromRow, Serialize, Deserialize, ToSchema)]
pub struct PortfolioItem {
    title: String,
    subtitle: String,
    image: Vec<String>,
    project_date: u32,
    role: String,
    client: Option<u32>, // a foreign key to the Clients db
    public_url: Option<String>,
    description : String,
    youtube_url: Option<String>,
    portfolio_type: PortfolioType
}
