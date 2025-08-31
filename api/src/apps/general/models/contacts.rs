/// The contact info for the site
pub struct SiteContact {
    id: i32,
    email: String,
    phone: String,
    address: Option<String>,
    facebook: Option<String>,
    twitter: Option<String>,
    instagram: Option<String>,
    dribble: Option<String>,
    behance: Option<String>
}

/// The contact info sent by public user to the owner
pub struct ContactPost {
    id: i32,
    name: String,
    email: String,
    message: String,
    created_at: String
}