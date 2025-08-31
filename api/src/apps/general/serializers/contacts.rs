use serde::{Deserialize, Serialize};
use utoipa::ToSchema;

#[derive(Serialize, Deserialize, Debug, ToSchema)]
pub struct ContactPostSerializer {
    pub name: String,
    pub email: String,
    pub message: String
}