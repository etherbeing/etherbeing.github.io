use actix_cors::Cors;

pub fn setup_cors() -> Cors {
    let mut cors = Cors::default().allow_any_method().allow_any_header();
    let frontend_urls = &std::env::var("FRONTEND_URL").unwrap_or_else(|_| {
        panic!("Frontend URLs aren't setup so nothing will be usable from browsers due to CORS")
    });
    for frontend_url in frontend_urls.split(",").collect::<Vec<&str>>() {
        cors = cors.allowed_origin(frontend_url.trim());
    }
    cors.supports_credentials().max_age(3600)
}
