from __future__ import annotations

import json
import os
from dataclasses import dataclass

import requests
from django.conf import settings

from .models import BlogEntry


@dataclass
class PublishResult:
    gist_id: str
    html_url: str
    social_results: dict[str, str]


def build_gist_files(content: str, category: str, social_networks: list[str]) -> dict[str, dict[str, str]]:
    return {
        "content.md": {"content": content},
        "metadata.json": {
            "content": json.dumps(
                {
                    "category": category,
                    "social_networks": social_networks,
                },
                indent=2,
            )
        },
    }


def get_publishing_token(user) -> str:
    token = getattr(user, "github_access_token", "") if user and getattr(user, "is_authenticated", False) else ""
    if token:
        return token
    return os.getenv("GITHUB_PUBLISH_ACCESS_TOKEN", "")


def publish_gist_post(*, user, title: str, content: str, category: str, social_networks: list[str]) -> PublishResult:
    token = get_publishing_token(user)
    if not token:
        raise ValueError("A GitHub publishing token is required to publish posts.")

    response = requests.post(
        "https://api.github.com/gists",
        headers={
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {token}",
            "User-Agent": os.getenv("GITHUB_USER", "etherbeing-site"),
        },
        json={
            "description": title,
            "public": True,
            "files": build_gist_files(content, category, social_networks),
        },
        timeout=20,
    )
    response.raise_for_status()
    gist_payload = response.json()
    BlogEntry.create_from_gist(gist_payload)
    return PublishResult(
        gist_id=str(gist_payload["id"]),
        html_url=gist_payload["html_url"],
        social_results=dispatch_social_notifications(
            title=title,
            category=category,
            gist_url=gist_payload["html_url"],
            social_networks=social_networks,
        ),
    )


def dispatch_social_notifications(*, title: str, category: str, gist_url: str, social_networks: list[str]) -> dict[str, str]:
    message = (
        f"New post published\n\n"
        f"Title: {title}\n"
        f"Category: {BlogEntry.Category(category).label if category in BlogEntry.Category.values else category}\n"
        f"Read it: {gist_url}"
    )
    results: dict[str, str] = {}

    for network in social_networks:
        try:
            if network == "telegram":
                notify_telegram(message)
            elif network == "discord":
                notify_discord(message)
            elif network == "whatsapp":
                notify_whatsapp(message)
            else:
                results[network] = "unsupported"
                continue
            results[network] = "sent"
        except Exception as error:  # pragma: no cover - captured for operator visibility
            results[network] = f"failed: {error}"
    return results


def notify_telegram(message: str) -> None:
    token = os.getenv("TELEGRAM_TOKEN", "")
    chat_id = os.getenv("TELEGRAM_TO", "")
    if not token or not chat_id:
        raise ValueError("Telegram publishing is not configured.")
    response = requests.post(
        f"https://api.telegram.org/bot{token}/sendMessage",
        json={"chat_id": chat_id, "text": message},
        timeout=20,
    )
    response.raise_for_status()


def notify_discord(message: str) -> None:
    webhook = os.getenv("DISCORD_WEBHOOK", "")
    if not webhook:
        raise ValueError("Discord publishing is not configured.")
    response = requests.post(
        webhook,
        json={"content": message},
        timeout=20,
    )
    response.raise_for_status()


def notify_whatsapp(message: str) -> None:
    base_url = os.getenv("EVOLUTION_API_BASE_URL", "").rstrip("/")
    instance = os.getenv("EVOLUTION_API_INSTANCE", "")
    token = os.getenv("EVOLUTION_API_TOKEN", "")
    chat_id = os.getenv("EVOLUTION_API_CHAT_ID", "")
    if not base_url or not instance or not token or not chat_id:
        raise ValueError("WhatsApp Evolution API publishing is not configured.")

    response = requests.post(
        f"{base_url}/message/sendText/{instance}",
        headers={"apikey": token},
        json={
            "number": chat_id,
            "text": message,
        },
        timeout=20,
    )
    response.raise_for_status()
