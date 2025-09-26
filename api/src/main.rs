mod apps;
mod controllers;
mod core;
mod serializers;

use actix_cors::Cors;
use actix_web::web::{self, Data};
use actix_web::{App, HttpResponse, HttpServer};
use async_graphql::http::GraphQLPlaygroundConfig;
use async_graphql::{EmptyMutation, EmptySubscription, Schema};
use core::settings::graphql::graphql_handler;
use cv_etherbeing::setup_cors;
use sqlx::postgres::PgPoolOptions;
use utoipa::OpenApi;
use utoipa_swagger_ui::SwaggerUi;

use crate::apps::demo_app::consumers::ws_index;
use crate::apps::general::controllers::about_me::get_info_about_me;
use crate::apps::general::controllers::contacts::contact;
use crate::apps::general::controllers::portfolio::{create_portfolio_item, get_portfolio};
use crate::apps::security::controllers::{login, logout, me, refresh, register};
use crate::core::settings::graphql::QueryRoot;
use crate::core::settings::swagger::ApiDoc;

#[actix_web::main]
async fn main() -> std::io::Result<()> {
    #[cfg(debug_assertions)]
    {
        dotenv::dotenv().ok();
    }

    #[cfg(not(debug_assertions))]
    {
        dotenv::from_filename(".env.production").ok();
    }
    let schema = Schema::build(QueryRoot, EmptyMutation, EmptySubscription).finish();

    let pool = PgPoolOptions::new()
        .connect(&std::env::var("DATABASE_URL").unwrap())
        .await
        .expect("Failed to connect to Postgres");
    HttpServer::new(move || {
        App::new()
            .wrap(setup_cors())
            .app_data(Data::new(pool.clone()))
            // authentications
            .service(me)
            .service(login)
            .service(logout)
            .service(refresh)
            .service(register)
            .service(get_info_about_me)
            .service(get_portfolio)
            .service(create_portfolio_item)
            // general
            // contacts
            .service(contact)
            // end contacts
            // end general
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
    .bind(("0.0.0.0", 8080))?
    .run()
    .await
}

async fn playground() -> HttpResponse {
    HttpResponse::Ok()
        .content_type("text/html; charset=utf-8")
        .body(async_graphql::http::playground_source(
            GraphQLPlaygroundConfig::new("/graphql"),
        ))
}
