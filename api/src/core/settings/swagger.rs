
use utoipa::OpenApi;


use crate::serializers::types::IndexResponse;


#[derive(OpenApi)]
#[openapi(
    paths(
        crate::controllers::base::index
    ), 
    components(
            schemas(
                IndexResponse
            )
        )
    )
]
pub struct ApiDoc;
