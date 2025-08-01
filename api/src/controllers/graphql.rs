use async_graphql::Object;


pub struct QueryRoot;

#[Object]
impl QueryRoot {
    async fn hello(&self) -> &str {
        "Hello, GraphQL!"
    }
}