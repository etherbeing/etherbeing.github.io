# Dockerfile
FROM rust:1.77 as builder

WORKDIR /app
COPY . .
RUN cargo build --release

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y ca-certificates && rm -rf /var/lib/apt/lists/*

COPY --from=builder /app/target/release/your-actix-app /usr/local/bin/actix-app

EXPOSE 8080

CMD ["actix-app"]
