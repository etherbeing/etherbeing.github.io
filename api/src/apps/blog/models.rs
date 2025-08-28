use crate::apps::security::models::User;

pub struct Category {
    name: String
}
pub struct Tag {
    name: String
}
pub struct  Comment {
    user: User,
    created_at: u32,
    message: String,
    replies: Vec<Comment>
}
/// Also a blog post
pub struct BlogEntry {
    title: String,
    subtitle: String,
    banner_image: String,
    content: String, // rich text content
    categories: Vec<Category>,
    tags: Vec<Tag>
}