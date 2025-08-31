use std::{collections::HashMap, env};

use actix_web::{
    HttpRequest, HttpResponse, Responder,
    cookie::{
        Cookie,
        time::{self, Duration},
    },
    get, post,
    web::{self, Data},
};
use chrono::Utc;

use crate::apps::security::{
    models::User,
    serializers::{LoginUser, RegisterUser},
    utils::jwt::{self, Claims, create_token, process_response, validate_jwt},
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
        (status=200, description="Authenticate the user"),
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
                        let access_token = jwt::create_token(
                            user.get_username(),
                            &secret_key,
                            Duration::minutes(15).whole_minutes(),
                        );
                        let refresh_token = jwt::create_token(
                            user.get_username(),
                            &secret_key,
                            Duration::days(15).whole_minutes(),
                        );
                        return HttpResponse::Ok()
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
                            )
                            .json({});
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

    match sqlx::query("INSERT INTO users(username, email, country, google, created_at, last_login) VALUES ($1, $2, $3, $4, $5, $6)")
        .bind(&payload.username)
        .bind(&payload.email)
        .bind(&payload.country)
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
                            return process_response(HttpResponse::Ok(), user);
                        },
                        Err(err) => {
                            println!("{:?}", err);
                            return HttpResponse::BadRequest().json({})
                        }
                    }
                },
                Err(err) => {
                    println!("{:?}", err);
                    return HttpResponse::BadRequest().json({})
                }
            }
        },
        Err(error) => {
            dbg!(error);
            return HttpResponse::BadRequest().json({})
        },
    }
}

#[utoipa::path(
    post,
    path="/api/auth/refresh",
    tag="authentication",
    responses(
        (status=200, description="Token refreshed"),
        (status=401, description="Not authorized to perform this action"),
    )
)]
#[post("/api/auth/refresh")]
pub async fn refresh(req: HttpRequest) -> impl Responder {
    let secret: String = env::var("SECRET_KEY").unwrap(); // TODO Please check how expensive is to check the env on each req
    if let Some(refresh_cookie) = req.cookie("refresh_token") {
        let refresh_token = refresh_cookie.value().to_string();
        if let Some(claims) = validate_jwt(&refresh_token, &secret) {
            let access_token = create_token(
                &claims.sub,
                &secret,
                time::Duration::minutes(15).whole_minutes(),
            );
            return HttpResponse::Ok()
                .cookie(
                    Cookie::build("Authorization", format!("Bearer {}", access_token))
                        .http_only(true)
                        .secure(false)
                        .finish(),
                )
                .json({});
        }
    }
    return HttpResponse::Unauthorized().json({});
}

#[utoipa::path(
    post,
    path="/api/auth/logout",
    tag="authentication",
    responses(
        (status=200, description="Auth logout"),
        (status=401, description="Not authorized to perform this action"),
    )
)]
#[post("/api/auth/logout")]
pub async fn logout(req: HttpRequest) -> impl Responder {
    let mut res = HttpResponse::Ok();
    let mut logged_out = false;
    let auth_cookie = req.cookie("Authorization");
    if let Some(mut cookie) = auth_cookie {
        cookie.make_removal();
        res.cookie(cookie);
        logged_out = true;
    }
    let refresh_cookie = req.cookie("refresh_token");
    if let Some(mut cookie) = refresh_cookie {
        cookie.make_removal();
        res.cookie(cookie);
        logged_out = true
    }
    if logged_out {
        return res.json({});
    } else {
        return HttpResponse::Unauthorized().json({});
    }
}
