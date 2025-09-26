# ---- Build stage ----
FROM node:20-alpine AS build

# Enable corepack so pnpm is available
RUN corepack enable

WORKDIR /app

COPY package.json pnpm-lock.yaml ./
RUN pnpm install --frozen-lockfile

COPY . .
RUN pnpm run build

# ---- Runtime stage ----
FROM node:20-alpine AS runtime

RUN corepack enable

WORKDIR /app

# Install only 'serve' to serve the static files
RUN pnpm add serve --global

# Copy build output
COPY --from=build /app/dist ./dist

EXPOSE 3000

CMD ["serve", "-s", "dist", "-l", "3000"]
