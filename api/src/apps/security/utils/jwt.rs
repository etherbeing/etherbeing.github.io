use std::env;

use actix::fut::{ready, Ready};
use actix_web::{Error, FromRequest};
use chrono::{Duration, Utc};
use jsonwebtoken::{decode, encode, DecodingKey, EncodingKey, Header, Validation};
use serde::{Deserialize, Serialize};


#[derive(Debug, Serialize, Deserialize)]
pub struct Claims {
    pub sub: String,
    pub exp: usize
}

pub fn create_jwt(user_id: &str, secret: &str) -> String {
    let expiration = Utc::now().checked_add_signed(Duration::hours(24)).unwrap().timestamp() as usize;
    let claims = Claims {
        sub: user_id.to_owned(),
        exp: expiration
    };
    encode(&Header::default(), &claims, &EncodingKey::from_secret(secret.as_ref())).expect("Token creation failed")
}
pub fn validate_jwt(token: &str, secret: &str) -> Option<Claims> {
    let validation = Validation::default();
    let result = decode::<Claims>(token, &DecodingKey::from_secret(secret.as_ref()), &validation);
    result.ok().map(|data| data.claims) 
}

impl FromRequest for Claims  {
    type Error = Error;
    type Future = Ready<Result<Self, Self::Error>>;

    fn from_request(req: &actix_web::HttpRequest, _payload: &mut actix_web::dev::Payload) -> Self::Future {
        let auth_header = req.headers().get("Authorization").and_then(|h| h.to_str().ok());
        if let Some(header_value) = auth_header {
            if let Some(token) = header_value.strip_prefix("Bearer ",) {
                println!("{:?}", auth_header);
                let secret = env::var("SECRET_KEY").unwrap();
                if let Some(claims) = validate_jwt(token, &secret) {
                    return ready(Ok(claims));
                }
            }
        }
        ready(Err(actix_web::error::ErrorUnauthorized("Invalid token")))
    }
}