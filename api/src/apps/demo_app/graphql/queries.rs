use async_graphql::Object;

use crate::core::settings::graphql::QueryRoot;

#[Object]
impl QueryRoot {
    async fn hello(&self) -> &str {
        "Hello, GraphQL!"
    }
}