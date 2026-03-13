# etherbeing official

[![Astro Build](https://img.shields.io/badge/frontend-Astro%205-ff5d01?logo=astro&logoColor=white)](#stack)
[![Django API](https://img.shields.io/badge/backend-Django%206-0c4b33?logo=django&logoColor=white)](#stack)
[![License: MIT](https://img.shields.io/badge/license-MIT-yellow.svg)](./LICENSE)
[![PWA Ready](https://img.shields.io/badge/pwa-enabled-0ea5e9)](#capabilities)

Open-source personal platform for `etherbeing`, combining a modern Astro frontend, a Django backend, GitHub-powered blog publishing, service acquisition flows, and a heavily customized admin experience.

## Overview

This project is built to operate as:

- A portfolio and personal site
- A GitHub-gist-backed blog
- A GitHub-repo-backed projects showcase
- A service catalog with acquisition requests
- A custom Django admin for site operations and publishing
- A PWA-capable frontend with offline-friendly caching

## Capabilities

- Dynamic homepage content served by the backend
- GitHub Gists treated as blog posts
- GitHub public repositories treated as project cards
- Cached GitHub API access to reduce rate-limit failures
- Frontend GitHub login with scoped permissions
- Admin GitHub login with elevated scopes for publishing and private resources
- Optional reCAPTCHA protection for admin login
- Rich-text publishing flow in admin that creates GitHub gists
- Social notification dispatch for newly published posts
- Service detail pages and service request tracking
- Custom branded Django admin theme and layouts
- Shared favicon/configuration driven from the backend
- PWA manifest and service worker support

## Stack

### Frontend

- Astro
- React
- Tailwind CSS
- TypeScript

### Backend

- Django
- Django REST Framework
- PostgreSQL
- Redis

### Integrations

- GitHub OAuth
- GitHub Gists API
- GitHub Repositories API
- Telegram notifications
- Discord notifications
- Evolution API basics for WhatsApp delivery

## Architecture

```text
Frontend (Astro + React)
  -> consumes Django API
  -> uses GitHub OAuth via frontend callback relay
  -> renders blog, projects, services, config, PWA

Backend (Django + DRF)
  -> stores site content, services, requests, publishing records
  -> syncs GitHub gists as blog entries
  -> syncs GitHub repos as projects
  -> publishes new posts as GitHub gists
  -> sends social notifications

Data / Infra
  -> PostgreSQL
  -> Redis
  -> Docker Compose for local dependencies
```

## Project Structure

```text
.
├── api/                  # Django backend
├── src/                  # Astro frontend source
├── public/               # Static assets and service worker
├── devops/               # Deployment and secrets-related support files
├── docker-compose.yml    # Local dev dependencies
└── start.sh              # Convenience full-stack startup
```

## Local Development

### 1. Start local dependencies

```bash
docker compose up -d postgres redis
```

### 2. Run migrations

```bash
cd api
python3 src/etherbeing/manage.py migrate
```

### 3. Seed initial site content

```bash
cd api
python3 src/etherbeing/manage.py init_site_content
```

### 4. Run the backend

```bash
cd api
python3 src/etherbeing/manage.py runserver 127.0.0.1:8000
```

### 5. Run the frontend

```bash
pnpm dev
```

Frontend default URL:

- `http://localhost:4321`

Backend default URL:

- `http://127.0.0.1:8000`

## Environment Notes

### Frontend

Useful frontend env values include:

- `PUBLIC_API_URL`
- `PUBLIC_SITE_URL`

### Backend

Useful backend env values include:

- `DJANGO_ENV_FILE`
- `DBNAME`
- `DBUSER`
- `DBPASS`
- `DBHOST`
- `DBPORT`
- `CORS_ALLOWED_ORIGINS`
- `CSRF_TRUSTED_ORIGINS`
- `GITHUB_OAUTH_CLIENT_ID`
- `GITHUB_OAUTH_CLIENT_SECRET`
- `GITHUB_OAUTH_REDIRECT_URI`
- `GITHUB_OAUTH_SCOPES`
- `GITHUB_FRONTEND_OAUTH_SCOPES`
- `GITHUB_COMMENT_OAUTH_SCOPES`
- `GITHUB_PUBLISH_ACCESS_TOKEN`
- `RECAPTCHA_SITE_KEY`
- `RECAPTCHA_SECRET_KEY`
- `RECAPTCHA_MIN_SCORE`
- `EVOLUTION_API_BASE_URL`
- `EVOLUTION_API_INSTANCE`
- `EVOLUTION_API_TOKEN`
- `EVOLUTION_API_CHAT_ID`

## Publishing Flow

The custom admin includes a dedicated publishing page for blog posts.

Current behavior:

- Admin user writes the post using a rich-text editor
- Post is published as a GitHub Gist
- Metadata is stored in the gist so the backend can categorize it
- A `PublishedPost` record is saved in Django admin
- Selected social networks are notified

Current social delivery support:

- Telegram
- Discord
- WhatsApp basics through Evolution API

## Deployment

This repository includes Docker Compose support for backend dependencies and a production-style API container.

High-level deployment flow:

1. Build and deploy the Django API with the correct production env file.
2. Run migrations.
3. Collect and serve media/static as configured by the backend.
4. Build and deploy the Astro frontend.
5. Point the frontend `PUBLIC_API_URL` to the deployed backend.
6. Configure GitHub OAuth callbacks for frontend and admin login flows.

At minimum, production requires:

- PostgreSQL
- Redis
- Django env secrets
- GitHub OAuth app configuration
- Optional reCAPTCHA keys
- Optional Telegram/Discord/WhatsApp notification credentials

## Admin Features

- Custom login page
- Optional reCAPTCHA protection
- GitHub OAuth admin login
- First-superuser bootstrap in debug mode
- Service request management
- Site-content management
- Publishing record management
- Rich blog publishing page

## Roadmap / TODO

The old strategy section is now tracked as executable product tasks.

### Blog Integrations

- [x] Telegram notifications
- [ ] WhatsApp publishing flow beyond the current Evolution API basics
- [ ] LinkedIn publishing
- [ ] Instagram publishing
- [ ] Facebook publishing
- [ ] YouTube publishing

### Content To Publish

- [x] Cybersecurity category
- [x] Software Development category
- [x] DevOps category
- [x] Philosophy category
- [x] Politics category
- [x] Project Ads category
- [x] Artificial Intelligence category
- [x] Researches category

### Other Services

- [x] MCP tools for AI
- [x] Pentesting and Bug Hunting
- [x] Software Development
- [x] OSINT
- [x] DevOps and Cluster Deployment
- [x] Marketing Tools
- [x] Content Generation AI tools

### Product Tasks

- [ ] Add direct LinkedIn publishing support from admin
- [ ] Add Instagram publishing support from admin
- [ ] Add Facebook publishing support from admin
- [ ] Add YouTube publishing support from admin
- [ ] Extend WhatsApp publishing from basic transport to a richer content flow
- [ ] Add preview rendering for published rich-text posts before gist creation
- [ ] Add scheduling support for social publishing
- [ ] Add retry/audit UI for failed social notifications
- [ ] Add richer analytics for posts, services, and acquisition funnels

## Testing

Backend:

```bash
cd api
python3 src/etherbeing/manage.py test apps.base -v 1
python3 src/etherbeing/manage.py check
```

Frontend:

```bash
pnpm build
```

## License

This project is open source and distributed under the [MIT License](./LICENSE).
