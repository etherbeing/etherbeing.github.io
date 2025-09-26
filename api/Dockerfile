# Dockerfile
FROM rust:1.90 as builder

ENV SQLX_OFFLINE=true

WORKDIR /app
COPY . .
RUN cargo build --release

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y ca-certificates && rm -rf /var/lib/apt/lists/*

COPY --from=builder /app/target/release/cv_etherbeing /usr/local/bin/cv_etherbeing

EXPOSE 8080

CMD ["cv_etherbeing"]
