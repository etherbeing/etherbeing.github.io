use actix::{Actor, StreamHandler};
use actix_web_actors::ws;


// WebSocket session actor
pub struct WebSocketRoot;

impl Actor for WebSocketRoot {
    type Context = ws::WebsocketContext<Self>;

    fn started(&mut self, ctx: &mut Self::Context) {
        ctx.text("WebSocket connected");
    }
}

impl StreamHandler<Result<ws::Message, ws::ProtocolError>> for WebSocketRoot {
    fn handle(&mut self, msg: Result<ws::Message, ws::ProtocolError>, ctx: &mut Self::Context) {
        match msg {
            Ok(ws::Message::Text(text)) => {
                ctx.text(format!("Echo: {}", text));
            }
            Ok(ws::Message::Ping(msg)) => {
                ctx.pong(&msg);
            }
            _ => (),
        }
    }
}
