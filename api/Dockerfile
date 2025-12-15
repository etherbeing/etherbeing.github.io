# syntax=docker/dockerfile:1.7
# NOTE The reason for picking up the next image version is because is the only one with no vulnerabilities at all
FROM python:3.15.0a2-alpine


# ---- system ----
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_SYSTEM_PYTHON=1 \
    UV_NO_CACHE=1

WORKDIR /app

# ---- system deps ----
RUN apk update && apk add --no-cache \
    build-base \
    libffi-dev \
    postgresql-dev \
    curl
# ---- install uv ----
ADD https://astral.sh/uv/0.9.17/install.sh /uv-installer.sh

RUN chmod +x /uv-installer.sh && sh /uv-installer.sh && rm /uv-installer.sh && cp -r $HOME/.local/bin/* /usr/local/bin/

# ---- dependencies ----
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev

# ---- app ----
COPY . .

# ---- runtime ----
EXPOSE 8000

WORKDIR /app/src/etherbeing

RUN yes yes | uv run manage.py collectstatic

ENTRYPOINT ["uv", "run","daphne", "-b", "0.0.0.0", "-p", "8000", "etherbeing.asgi:application"]
