# Dockerfile
FROM rust:1.90

ENV SQLX_OFFLINE=true

WORKDIR /app
COPY . .
RUN cargo build --release

RUN apt-get update && apt-get install -y ca-certificates && rm -rf /var/lib/apt/lists/*

RUN cp /app/target/release/cv_etherbeing /usr/local/bin/cv_etherbeing

EXPOSE 8080

RUN cargo install sqlx

RUN chmod +x /app/entrypoint.sh

ENTRYPOINT /app/entrypoint.sh
