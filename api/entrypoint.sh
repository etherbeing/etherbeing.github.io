#!/bin/sh
uv run manage.py migrate
uv run daphne -b 0.0.0.0 -p "${API_PORT:-7000}" etherbeing.asgi:application
