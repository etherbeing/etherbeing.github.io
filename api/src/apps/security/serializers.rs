use serde::{Deserialize, Serialize};
use utoipa::ToSchema;

#[derive(Serialize, Deserialize, Debug, ToSchema)]
pub struct LoginUser {
    /// can be also the email
    pub username: String,
    pub password: String,
}

#[derive(Serialize, Deserialize, Debug, ToSchema)]
pub struct RegisterUser {
    pub username: String,
    pub email: String,
    pub password: String,
    pub country: i32,
    pub google: Option<String>,
}

#[derive(Serialize, Deserialize, Debug, ToSchema)]
pub struct EmptyResponse {
}