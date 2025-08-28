use serde::{Deserialize, Serialize};
use utoipa::ToSchema;

#[derive(Serialize, Deserialize, Debug, ToSchema)]
pub struct LoginUser {
    /// can be also the email
    pub username: String,
    pub password: String,
}
#[derive(Serialize, Deserialize, Debug, ToSchema)]
pub struct LoginResponse {
    pub access_token: String,
    pub refresh_token: String,
}

#[derive(Serialize, Deserialize, Debug, ToSchema)]
pub struct RegisterUser {
    pub username: String,
    pub email: String,
    pub password: String,
    pub phone: String,
    pub google: Option<String>,
}

#[derive(Serialize, Deserialize, Debug, ToSchema)]
pub struct EmptyResponse {
}