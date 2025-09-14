use std::collections::HashMap;

use actix_multipart::form::MultipartForm;
use actix_web::{get, put, web::Data, HttpResponse, Responder};
use chrono::{Date, NaiveDate, NaiveDateTime, TimeZone, Utc};
use sqlx::PgPool;

use crate::apps::{general::serializers::portfolio::{PortfolioItemMetadataSerializer, PortfolioItemRawSerializer, PortfolioItemResponseSerializer, PortfolioItemSerializer, PortfolioType}, security::utils::jwt::Claims};

#[
    utoipa::path(
        get, 
        path="/api/public/portfolio/", 
        tag="public", 
        responses(
            (status=200, body=[PortfolioItemResponseSerializer])
        )
    )
]
#[get("/api/public/portfolio/")]
pub async fn get_portfolio(pool: Data<PgPool>) -> impl Responder {
    let mut res = Vec::new();
    let mut d = HashMap::new();
    d.insert("msg", "hello portfolios");
    res.push(d);
    HttpResponse::Ok().json(res)
}
#[utoipa::path(
    put,
    tag="admin",
    path="/api/admin/portfolio/",
    request_body(
        content=PortfolioItemRawSerializer,
        content_type="multipart/form-data"
    ),
    responses(
        (status=403, description="Credentials not valid for the current request"),
        (status=201, description="Portfolio Item created successfully")
    ),
    security(
        ("bearer_auth" = [])
    )
)]
#[put("/api/admin/portfolio/")]
pub async fn create_portfolio_item(pool: Data<PgPool>, claims: Claims, MultipartForm(payload): MultipartForm<PortfolioItemSerializer>) -> impl Responder{
    let pt =  match &payload.metadata.portfolio_type {
        PortfolioType::SimpleImage=>{
            "SimpleImage"
        },
        PortfolioType::SimpleVideo=>{
            "SimpleVideo"
        },
        PortfolioType::Detailed=>{
            "Detailed"
        }
    };
    match sqlx::query("INSERT INTO portfolio_item (title,subtitle,image,project_date,role,client,public_url,description,youtube_url,portfolio_type) VALUES ($1,$2,$3,$4,$5,$6,$7,$8,$9,$10)")
        .bind(&payload.metadata.title)
        .bind(&payload.metadata.subtitle)
        .bind("image uploaded")
        .bind(&payload.metadata.project_date)
        .bind(&payload.metadata.role)
        .bind(&payload.metadata.client.id)
        .bind(&payload.metadata.public_url)
        .bind(&payload.metadata.description)
        .bind(&payload.metadata.youtube_url)
        .bind(pt)
        .execute(pool.get_ref()).await {
            Ok(res)=>{
                println!("{:?}", res);
                HttpResponse::Ok().json({})
            },
            Err(err)=>{
                println!("{:?}", err);
                HttpResponse::InternalServerError().json({})
            }
        }
}  