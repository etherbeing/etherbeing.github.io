from __future__ import annotations

import os
from http import HTTPMethod
from typing import Any

import requests
from django.core.cache import cache


GITHUB_API_BASE = "https://api.github.com/"
GITHUB_CACHE_TIMEOUT = 60 * 15


def fetch_github_json(path_or_url: str, cache_key: str) -> Any:
    if cached := cache.get(cache_key):
        return cached

    if path_or_url.startswith("http://") or path_or_url.startswith("https://"):
        url = path_or_url
    else:
        url = f"{GITHUB_API_BASE}{path_or_url}"

    response = requests.request(
        HTTPMethod.GET,
        url,
        headers={
            "Accept": "application/vnd.github+json",
            "User-Agent": os.getenv("GITHUB_USER", "etherbeing-site"),
        },
        timeout=15,
    )
    response.raise_for_status()
    payload = response.json()
    cache.set(cache_key, payload, timeout=GITHUB_CACHE_TIMEOUT)
    return payload
