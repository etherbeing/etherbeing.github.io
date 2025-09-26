# ---- Build stage ----
FROM node:20-alpine AS build

RUN corepack enable

WORKDIR /app

COPY package.json pnpm-lock.yaml ./
RUN pnpm install --frozen-lockfile

COPY . .
RUN pnpm run build

# ---- Runtime stage ----
FROM node:20-alpine AS runtime

WORKDIR /app

# Only copy built output and package.json for minimal runtime
COPY --from=build /app/dist ./dist
COPY package.json pnpm-lock.yaml ./

# Install only serve locally (no dev deps, no source)
RUN corepack enable && pnpm add serve

EXPOSE 3000

CMD ["npx", "serve", "-s", "dist", "-l", "3000"]
