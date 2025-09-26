# Dockerfile
FROM rust:1.90 as builder

ENV SQLX_OFFLINE=true

WORKDIR /app
COPY . .
RUN cargo build --release

FROM rust:1.90

RUN apt-get update && apt-get install -y ca-certificates && rm -rf /var/lib/apt/lists/*

COPY --from=builder /app/target/release/cv_etherbeing /usr/local/bin/cv_etherbeing

EXPOSE 8080

RUN cargo install sqlx-cli --no-default-features --features native-tls,postgres

RUN chmod +x /app/entrypoint.sh

ENTRYPOINT /app/entrypoint.sh
