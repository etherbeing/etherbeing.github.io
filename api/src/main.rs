mod controllers;
mod serializers;
mod core;
mod apps;

use actix_cors::Cors;
use actix_web::web::{self, Data};
use actix_web::{App, HttpResponse, HttpServer};
use async_graphql::http::GraphQLPlaygroundConfig;
use async_graphql::{EmptyMutation, EmptySubscription, Schema};
use core::settings::graphql::graphql_handler;
use sqlx::postgres::PgPoolOptions;
use utoipa::OpenApi;
use utoipa_swagger_ui::SwaggerUi;

use crate::apps::demo_app::consumers::ws_index;
use crate::apps::security::controllers::{login, me, register};
use crate::controllers::base::*;
use crate::core::settings::graphql::QueryRoot;
use crate::core::settings::swagger::ApiDoc;

#[actix_web::main]
async fn main() -> std::io::Result<()> {
    dotenv::dotenv().ok();
    let schema = Schema::build(QueryRoot, EmptyMutation, EmptySubscription).finish();

    let pool = PgPoolOptions::new()
        .connect(&std::env::var("DATABASE_URL").unwrap())
        .await
        .expect("Failed to connect to Postgres");
    HttpServer::new(move || {
        App::new()
            .wrap(
                Cors::default()
                    .allow_any_method()
                    .allow_any_header()
                    .allowed_origin(&std::env::var("FRONTEND_URL").unwrap())
                    .supports_credentials()
                    .max_age(3600),
            )
            .app_data(Data::new(pool.clone()))
            .service(add_message)
            .service(get_message)
            .service(me)
            .service(login)
            .service(register)
            .service(index)
            .service(ws_index)
            .service(
                web::scope("/graphql")
                    .app_data(web::Data::new(schema.clone()))
                    .route("", web::post().to(graphql_handler)),
            )
            .route("/playground", web::get().to(playground))
            .service(
                SwaggerUi::new("/swagger-ui/{_:.*}")
                    .url("/api-doc/openapi.json", ApiDoc::openapi()),
            )
    })
    .bind(("127.0.0.1", 8080))?
    .run()
    .await
}


async fn playground() -> HttpResponse {
    HttpResponse::Ok()
        .content_type("text/html; charset=utf-8")
        .body(async_graphql::http::playground_source(GraphQLPlaygroundConfig::new("/graphql")))
}