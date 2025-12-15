#!/bin/sh
uv run manage.py migrate
uv run daphne -b 0.0.0.0 -p 8000 etherbeing.asgi:application