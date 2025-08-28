use super::portfolio::PortfolioItem;

pub struct Client {
    name: String,
    role: Option<String>,
    avatar: Option<String>,
    projects: Vec<PortfolioItem>,
    logo: Vec<String>
}