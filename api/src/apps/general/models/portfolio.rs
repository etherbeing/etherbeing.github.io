use super::clients::{Client};

pub struct PortfolioItem {
    title: String,
    subtitle: String,
    image: Vec<String>,
    project_date: u32,
    role: String,
    client: Option<Client>,
    public_url: Option<String>,
    description : String,
    youtube_url: Option<String>,
}
