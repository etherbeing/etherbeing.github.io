use serde::{Deserialize, Serialize};
use utoipa::ToSchema;

use super::portfolio::PortfolioItem;

#[derive(Serialize, Debug, ToSchema, Deserialize)]
pub struct Client {
    name: String,
    role: Option<String>,
    avatar: Option<String>,
    projects: Vec<PortfolioItem>,
    logo: Vec<String>
}