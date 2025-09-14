use chrono::{Date, NaiveDate};
use sqlx::prelude::FromRow;
use utoipa::ToSchema;


#[derive(FromRow, Debug)]
pub struct PortfolioItem {
    title: String,
    subtitle: String,
    image: String,
    project_date: NaiveDate,
    role: String,
    client: i64, // a foreign key to the Clients db
    public_url: Option<String>,
    description : String,
    youtube_url: Option<String>,
    portfolio_type: i8
}