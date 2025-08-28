use actix_web::web;
use async_graphql::*;
use async_graphql_actix_web::{GraphQLRequest, GraphQLResponse};


pub struct QueryRoot;


pub async fn graphql_handler(
    schema: web::Data<Schema<QueryRoot, EmptyMutation, EmptySubscription>>,
    req: GraphQLRequest,
) -> GraphQLResponse {
    schema.execute(req.into_inner()).await.into()
}
