use actix_multipart::form::json::Json;
use actix_multipart::form::tempfile::TempFile;
use actix_multipart::form::MultipartForm;
use actix_web::web::Data;
use serde::{Deserialize, Serialize};
use sqlx;
use sqlx::PgPool;
use sqlx::prelude::FromRow;
use utoipa::ToSchema;

use crate::apps::general::models::portfolio::PortfolioItem;

#[derive(Serialize, Debug, ToSchema, Deserialize)]
pub struct ClientMetadataSerializer {
    pub name: String,
    pub role: Option<String>,
}

#[derive(MultipartForm, Debug)]
pub struct ClientMultipartSerializer {
    #[multipart(limit = "10mb")]
    pub avatar: TempFile,
    #[multipart(limit = "10mb")]
    pub logo: TempFile,
    pub metadata: Json<ClientMetadataSerializer>,
}

#[derive(Serialize, Debug, ToSchema, Deserialize)]
pub struct ClientSerializer {
    #[schema(read_only)]
    pub id: i64,
    pub name: String,
    pub role: Option<String>,
    pub avatar: Option<String>,
    pub logo: String,
}

impl ClientSerializer {
    pub async fn portfolio_items(&self, pool: Data<PgPool>) -> Vec<PortfolioItem> {
        match sqlx::query_as::<_, PortfolioItem>("SELECT * FROM portfolio_item WHERE client=$0")
            .bind(self.id)
            .fetch_all(pool.get_ref())
            .await
        {
            Ok(items) => {
                println!("{:?}", items)
            }
            Err(err) => {
                println!("{:?}", err)
            }
        }
        return Vec::new();
    }
}
