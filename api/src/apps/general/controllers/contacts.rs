use crate::apps::general::models::contacts::ContactPost;
use crate::apps::general::serializers::contacts::ContactPostSerializer;

use actix_web::{
    HttpResponse, Responder, post,
    web::{self, Data},
};
use chrono::{Date, Utc};
use sqlx::PgPool;

#[utoipa::path(
    post,
    path="/api/contact/",
    tag="contact",
    responses(
        (status=200, description="Contact us"),
        (status=403, description="Forbidden response"),
    ),
)]
#[post("/api/contact/")]
pub async fn contact(
    pool: Data<PgPool>,
    payload: web::Json<ContactPostSerializer>,
) -> impl Responder {
    let created_at = Utc::now().timestamp();
    match sqlx::query(
        "INSERT INTO contact_posts (email,name,message,created_at) VALUES ($1, $2, $3, $4)",
    )
    .bind(&payload.email)
    .bind(&payload.name)
    .bind(&payload.message)
    .bind(created_at)
    .execute(pool.get_ref())
    .await
    {
        Ok(val) => {
            println!("{:?}", val);

            HttpResponse::Ok().json({})
        }
        Err(val) => {
            println!("{}", val);
            HttpResponse::InternalServerError().json({})
        }
    }
}
