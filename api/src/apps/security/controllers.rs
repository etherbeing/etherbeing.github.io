use std::{collections::HashMap, env};

use actix_web::{
    HttpResponse, Responder, get, post,
    web::{self, Data},
};
use chrono::Utc;

use crate::apps::security::{
    models::User,
    serializers::{LoginResponse, LoginUser, RegisterUser},
    utils::jwt::{self, Claims},
};

#[utoipa::path(
    post,
    path="/api/auth/login",
    tag="authentication",
    request_body(
        content(
            (LoginUser,)
        )
    ),
    responses(
        (status=200, description="Authenticate the user", body=LoginResponse),
        (status=403, description="Forbidden response"),
    )
)]
#[post("/api/auth/login")]
pub async fn login(pool: Data<sqlx::PgPool>, payload: web::Json<LoginUser>) -> impl Responder {
    match sqlx::query_as::<_, User>("SELECT * FROM users where username = $1 or email = $1")
        .bind(&payload.username)
        .fetch_one(pool.get_ref())
        .await
    {
        Ok(user) => {
            /* Now we need to evaluate the user password to see whether or not is valid TODO */
            if user.check_password(payload.password.clone()) {
                match env::var("SECRET_KEY") {
                    Ok(secret_key) => {
                        let access_token = jwt::create_jwt(user.get_username(), &secret_key);
                        let response = LoginResponse {
                            access_token: access_token,
                            refresh_token: String::new(),
                        };
                        return HttpResponse::Ok().json(response);
                    }
                    Err(_) => {
                        return HttpResponse::InternalServerError().json({});
                    }
                }
            } else {
                return HttpResponse::Forbidden().json({});
            }
        }
        Err(err) => {
            println!("{:?}", err);
            return HttpResponse::Forbidden().json({});
        }
    }
}

#[utoipa::path(
    get,
    path="/api/auth/me",
    tag="authentication",
    responses(
        (status=200, description="Get the current user details", body=LoginUser)
    ),
    security(
        ("bearer_auth" = [])
    )
)]
#[get("/api/auth/me")]
pub async fn me(pool: Data<sqlx::PgPool>, claims: Claims) -> impl Responder {
    match sqlx::query_as::<_, User>("SELECT * FROM users where username = $1")
        .bind(claims.sub)
        .fetch_one(pool.get_ref())
        .await
    {
        Ok(user) => HttpResponse::Ok().json(HashMap::from([
            ("id", &user.id.to_string()),
            ("username", user.get_username()),
        ])),
        Err(_) => HttpResponse::BadRequest().json({}),
    }
}

#[utoipa::path(
    post,
    path="/api/auth/register",
    tag="authentication",
    responses(
        (status=200, description="Get the current user details")
    ),
    request_body(
        content(
            (RegisterUser, )
        )
    )
)]
#[post("/api/auth/register")]
pub async fn register(
    pool: Data<sqlx::PgPool>,
    payload: web::Json<RegisterUser>,
) -> impl Responder {
    // let result =  sqlx::query_as::<_, User>("SELECT id, username, email FROM users where id = $1").bind(payload.id).fetch_one(pool.get_ref()).await;
    let current_date = Utc::now();

    match sqlx::query("INSERT INTO users(username, email, phone, google, created_at, last_login) VALUES ($1, $2, $3, $4, $5, $6)")
        .bind(&payload.username)
        .bind(&payload.email)
        .bind(&payload.phone)
        .bind(&payload.google)
        .bind(current_date.timestamp())
        .bind(current_date.timestamp())
        .execute(pool.get_ref())
        .await
    {
        Ok(value) => {
            println!("{:?}",value);
            match sqlx::query_as::<_, User>("SELECT * FROM users WHERE username=$1").bind(&payload.username).fetch_one(pool.get_ref()).await {
                Ok(mut user) => {
                    user = user.commit_password(payload.password.clone());
                    match sqlx::query("UPDATE users SET password=$1 WHERE username=$2").bind(user.get_password()).bind(user.get_username()).execute(pool.get_ref()).await {
                        Ok(val) => {
                            println!("{:?}", val);
                            return HttpResponse::Ok()
                        },
                        Err(err) => {
                            println!("{:?}", err);
                            return HttpResponse::BadRequest()
                        }
                    }
                },
                Err(err) => {
                    println!("{:?}", err);
                    return HttpResponse::BadRequest()
                }
            }
        },
        Err(error) => {
            dbg!(error);
            return HttpResponse::BadRequest()
        },
    }
}
