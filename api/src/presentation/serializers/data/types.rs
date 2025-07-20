use utoipa::ToSchema;
use serde::{Deserialize, Serialize};

#[derive(Serialize, Deserialize, ToSchema)]
pub struct Message {
    pub id: i32,
    pub content: String,
}

#[derive(serde::Serialize, ToSchema)]
pub struct IndexResponse {
    pub message: String,
}
