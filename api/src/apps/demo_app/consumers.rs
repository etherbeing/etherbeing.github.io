// Consumers for this app (Websocket controllers)
use actix_web::{get, web, Responder};
use actix_web_actors::ws;

use crate::core::network::websocket::base::WebSocketRoot;

#[get("/ws/")]
pub async fn ws_index(req: actix_web::HttpRequest, stream: web::Payload) -> impl Responder {
    ws::start(WebSocketRoot {}, &req, stream)
}
