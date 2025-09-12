use actix_web::{HttpResponse, Responder, get, web::Data};
use sqlx::PgPool;

use super::super::models::about_me::AboutMe;

#[utoipa::path(
    get,
    path="/api/public/about/",
    tag="public",
    responses(
        (status=200, description="Obtain general values that describe the owner of the site and the site itself"),
    ),
)]
#[get("/api/public/about/")]
pub async fn get_info_about_me(pool: Data<PgPool>) -> impl Responder {
    match sqlx::query_as::<_, AboutMe>("SELECT * FROM public_about_me LIMIT 1")
        .fetch_one(pool.get_ref())
        .await
    {
        Ok(info) => {
            println!("{:?}", info);
            return HttpResponse::Ok().json(info);
        }
        Err(err) => {
            println!("{:?}", err);
            return HttpResponse::InternalServerError().json({});
        }
    }
}

// TODO implement the update protected by JWT so we can update it from the frontend instead of manually in the DB