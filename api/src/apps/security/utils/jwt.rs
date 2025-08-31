use std::env;

use actix::fut::{Ready, ready};
use actix_web::{cookie::Cookie, Error, FromRequest, HttpResponse, HttpResponseBuilder};
use chrono::{Duration, Utc};
use jsonwebtoken::{DecodingKey, EncodingKey, Header, Validation, decode, encode};
use serde::{Deserialize, Serialize};

use crate::apps::security::models::User;

#[derive(Debug, Serialize, Deserialize)]
pub struct Claims {
    pub sub: String,
    pub exp: usize,
}

pub fn create_token(user_id: &str, secret: &str, minutes: i64) -> String {
    let expiration = Utc::now()
        .checked_add_signed(Duration::minutes(minutes))
        .unwrap()
        .timestamp() as usize;
    let claims = Claims {
        sub: user_id.to_owned(),
        exp: expiration,
    };
    encode(
        &Header::default(),
        &claims,
        &EncodingKey::from_secret(secret.as_ref()),
    )
    .expect("Token creation failed")
}
pub fn validate_jwt(token: &str, secret: &str) -> Option<Claims> {
    let validation = Validation::default();
    let result = decode::<Claims>(
        token,
        &DecodingKey::from_secret(secret.as_ref()),
        &validation,
    );
    result.ok().map(|data| data.claims)
}

impl FromRequest for Claims {
    type Error = Error;
    type Future = Ready<Result<Self, Self::Error>>;

    /// Implement automatic authentication from the cookies
    fn from_request(
        req: &actix_web::HttpRequest,
        _payload: &mut actix_web::dev::Payload,
    ) -> Self::Future {
        let secret: String = env::var("SECRET_KEY").unwrap(); // TODO Please check how expensive is to check the env on each req
        if let Some(authorization_cookie) = req.cookie("Authorization") {
            let bearer_token = authorization_cookie.value().to_string();
            if let Some(token) = bearer_token.strip_prefix("Bearer ") {
                if let Some(claims) = validate_jwt(token, &secret) {
                    return ready(Ok(claims));
                }
            }
        }
        return ready(Err(actix_web::error::ErrorUnauthorized("Invalid token")));
    }
}

pub fn process_response(mut response: HttpResponseBuilder, user: User) -> HttpResponse {
    match env::var("SECRET_KEY") {
        Ok(secret_key) => {
            let access_token = create_token(
                user.get_username(),
                &secret_key,
                actix_web::cookie::time::Duration::minutes(15).whole_minutes(),
            );
            let refresh_token = create_token(
                user.get_username(),
                &secret_key,
                actix_web::cookie::time::Duration::days(15).whole_minutes(),
            );
            return response
                .cookie(
                    Cookie::build("refresh_token", refresh_token)
                        .http_only(true)
                        .secure(false)
                        .path("/")
                        .finish(),
                )
                .cookie(
                    Cookie::build("Authorization", format!("Bearer {}", &access_token))
                        .http_only(true)
                        .secure(false)
                        .path("/")
                        .finish(),
                ).json({});
        }
        Err(_) => {
            return HttpResponse::InternalServerError().json({});
        }
    }
}
