use actix_web::{get, post, web::{self, Data}, HttpResponse, Responder};

use crate::presentation::serializers::data::types::{IndexResponse, Message};


#[post("/message")]
pub async fn add_message(pool: Data<sqlx::PgPool>, msg: web::Json<Message>) -> impl Responder {
    let res = sqlx::query!(
        "INSERT INTO messages (content) VALUES ($1) RETURNING id",
        msg.content
    )
    .fetch_one(pool.get_ref())
    .await;

    match res {
        Ok(record) => HttpResponse::Ok().json(Message {
            id: record.id,
            content: msg.content.clone(),
        }),
        Err(e) => {
            eprintln!("DB error: {:?}", e);
            HttpResponse::InternalServerError().body("DB error")
        }
    }
}

#[get("/message/{id}")]
pub async fn get_message(pool: Data<sqlx::PgPool>, id: web::Path<i32>) -> impl Responder {
    let res = sqlx::query_as!(
        Message,
        "SELECT id, content FROM messages WHERE id = $1",
        *id
    )
    .fetch_one(pool.get_ref())
    .await;

    match res {
        Ok(msg) => HttpResponse::Ok().json(msg),
        Err(_) => HttpResponse::NotFound().body("Not found"),
    }
}

#[utoipa::path(
    get,
    path="/",
    responses(
        (status=200, description="Main page", body=IndexResponse)
    )
)]
#[get("/")]
pub async fn index(_pool: Data<sqlx::PgPool>) -> impl Responder {
    HttpResponse::Ok().json(
        IndexResponse{
            message: "hola mundo".to_string()
        }
    )
}
