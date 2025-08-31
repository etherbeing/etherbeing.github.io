use utoipa::openapi::security::SecurityScheme::Http;
use utoipa::{OpenApi, openapi::security::HttpBuilder};

use crate::apps::general::serializers::contacts::ContactPostSerializer;
use crate::apps::security::serializers::RegisterUser;
use crate::{apps::security::serializers::LoginUser, serializers::types::IndexResponse};

struct SecurityAddon;

impl utoipa::Modify for SecurityAddon {
    fn modify(&self, openapi: &mut utoipa::openapi::OpenApi) {
        openapi.components = Some(
            utoipa::openapi::ComponentsBuilder::new()
                .security_scheme(
                    "bearer_auth",
                    Http(
                        HttpBuilder::new()
                            .scheme(utoipa::openapi::security::HttpAuthScheme::Bearer)
                            .bearer_format("JWT")
                            .build(),
                    ),
                )
                .schema_from::<IndexResponse>()
                .schema_from::<LoginUser>()
                .schema_from::<RegisterUser>()
                .schema_from::<ContactPostSerializer>()
                .build(),
        )
    }
}

#[derive(OpenApi)]
#[openapi(
    info(
        title = "Etherbeing CV",
        description = "Personal Esteban Chacon's website",
        contact(
            name = "Esteban Chacon Martin",
            email = "etherbeing99@proton.me",
            url = "https://etherbeing.github.io"
        ),
        license(name = "MIT (Attribution Required)", url = "TODO")
    ),
    paths(
        crate::apps::security::controllers::login,
        crate::apps::security::controllers::logout,
        crate::apps::security::controllers::refresh,
        crate::apps::security::controllers::register,
        crate::apps::security::controllers::me,
        crate::apps::general::controllers::contacts::contact
    ),
    modifiers(&SecurityAddon),
)]
pub struct ApiDoc;
