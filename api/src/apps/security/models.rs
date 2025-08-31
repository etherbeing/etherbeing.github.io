
use argon2::{
    Argon2, PasswordHash, PasswordHasher, PasswordVerifier,
    password_hash::{SaltString, rand_core::OsRng},
};
use serde::{Deserialize, Serialize};
use utoipa::ToSchema;

#[derive(sqlx::FromRow, Serialize, Deserialize, Debug, ToSchema)]
pub struct User {
    pub id: i32,
    username: String,
    password: Option<String>,
    email: String,
    country: i32,
    google: Option<String>, // Token for google auth
    created_at: i64,
    last_login: i64,
}
impl User {
    /// Hash the current user password and store it given a DB connection pool, it borrows the instance so the user is not accidentally used before the hashing is finished
    pub fn hash_password(&self) -> String {
        let salt = SaltString::generate(&mut OsRng);
        let argon2 = Argon2::default();
        let password = self.password.as_ref().unwrap().as_bytes();
        let hashed_password = argon2.hash_password(password, &salt).unwrap().to_string();
        let hasher = PasswordHash::new(&hashed_password).unwrap();
        argon2.verify_password(password, &hasher).unwrap();
        return hashed_password;
    }
    pub fn check_password(&self, password: String) -> bool {
        let hasher = PasswordHash::new(self.password.as_ref().unwrap().as_ref()).unwrap();
        let argon2 = Argon2::default();
        match argon2.verify_password(password.as_bytes(), &hasher) {
            Ok(_) => true,
            Err(_) => false,
        }
    }
    pub fn commit_password(mut self, raw_password: String) -> Self {
        self.password = Some(raw_password);
        self.password = Some(self.hash_password());
        return self;
    }
    pub fn get_password(&self,) -> &String {
        return self.password.as_ref().unwrap();
    }
    pub fn get_username(&self, ) -> &String {
        return &self.username;
    }
}
