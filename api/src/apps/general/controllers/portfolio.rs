use std::collections::HashMap;

use actix_web::{HttpResponse, Responder, get, web::Data};
use sqlx::PgPool;

use super::super::models::portfolio::PortfolioItem;

#[
    utoipa::path(
        get, 
        path="/api/public/portfolio/", 
        tag="public", 
        responses(
            (status=200, body=[PortfolioItem])
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
