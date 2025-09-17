use actix_multipart::form::{MultipartForm, json::Json, tempfile::TempFile};
use chrono::NaiveDate;
use serde::{Deserialize, Serialize};
use utoipa::ToSchema;

use super::client::ClientSerializer;

#[derive(ToSchema, Serialize, Debug, Deserialize)]
pub enum PortfolioType {
    Detailed,    // Portfolio 2
    SimpleImage, // Is just part of the image gallery not a page by itself
    SimpleVideo, // Is just part of the image gallery not a page by itself but it renders a video
}

#[derive(Debug, Deserialize, ToSchema, Serialize)]
pub struct PortfolioItemResponseSerializer {
    pub title: String,
    pub subtitle: String,
    pub image_url: String,
    pub project_date: NaiveDate,
    pub role: String,
    pub client: ClientSerializer, // a foreign key to the Clients db
    pub public_url: Option<String>,
    pub description: String,
    pub youtube_url: Option<String>,
    pub portfolio_type: PortfolioType,
}

#[derive(Debug, Deserialize, ToSchema, Serialize)]
pub struct PortfolioItemMetadataSerializer {
    pub title: String,
    pub subtitle: String,
    pub project_date: NaiveDate,
    pub role: String,
    pub client: ClientSerializer, // a foreign key to the Clients db
    pub public_url: Option<String>,
    pub description: String,
    pub youtube_url: Option<String>,
    pub portfolio_type: PortfolioType,
}

#[derive(Debug, MultipartForm)]
pub struct PortfolioItemSerializer {
    #[multipart(limit = "10mb")]
    pub image: TempFile,
    pub metadata: Json<PortfolioItemMetadataSerializer>,
}
#[derive(Debug, ToSchema, Serialize, Deserialize)]
pub struct PortfolioItemRawSerializer {
    #[schema(value_type=String, format=Binary)]
    pub image: String,
    pub metadata: PortfolioItemMetadataSerializer,
}
// #[derive(Debug, Deserialize)]
// struct Metadata {
//     name: String,
// }

// #[derive(Debug, MultipartForm)]
// struct UploadForm {
//     #[multipart(limit = "100MB")]
//     file: TempFile,
//     json: MpJson<Metadata>,
// }
