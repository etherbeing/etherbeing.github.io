
use utoipa::OpenApi;


use crate::presentation::serializers::data::types::IndexResponse;


#[derive(OpenApi)]
#[openapi(
    paths(
        crate::presentation::controllers::data::base::index
    ), 
    components(
            schemas(
                IndexResponse
            )
        )
    )
]
pub struct ApiDoc;
