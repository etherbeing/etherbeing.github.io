import secrets
from dataclasses import dataclass
from urllib.parse import urlencode

import requests
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model, login
from django.http import HttpRequest, HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.http import url_has_allowed_host_and_scheme


GITHUB_AUTHORIZE_URL = "https://github.com/login/oauth/authorize"
GITHUB_ACCESS_TOKEN_URL = "https://github.com/login/oauth/access_token"
GITHUB_API_URL = "https://api.github.com"
RECAPTCHA_VERIFY_URL = "https://www.google.com/recaptcha/api/siteverify"


@dataclass(frozen=True)
class RecaptchaVerificationResult:
    success: bool
    score: float = 1.0
    action: str = ""


def recaptcha_is_enabled() -> bool:
    return bool(settings.RECAPTCHA_SITE_KEY and settings.RECAPTCHA_SECRET_KEY)


def github_oauth_is_enabled() -> bool:
    return bool(settings.GITHUB_OAUTH_CLIENT_ID and settings.GITHUB_OAUTH_CLIENT_SECRET)


def verify_recaptcha_token(
    token: str,
    *,
    action: str = "",
    remoteip: str | None = None,
) -> RecaptchaVerificationResult:
    if not recaptcha_is_enabled():
        return RecaptchaVerificationResult(success=True, score=1.0, action=action)
    if not token:
        return RecaptchaVerificationResult(success=False, score=0.0, action="")

    response = requests.post(
        RECAPTCHA_VERIFY_URL,
        data={
            "secret": settings.RECAPTCHA_SECRET_KEY,
            "response": token,
            "remoteip": remoteip or "",
        },
        timeout=10,
    )
    payload = response.json()
    return RecaptchaVerificationResult(
        success=bool(payload.get("success")),
        score=float(payload.get("score", 0.0)),
        action=str(payload.get("action") or ""),
    )


def build_github_redirect_uri(request: HttpRequest) -> str:
    if settings.GITHUB_OAUTH_REDIRECT_URI:
        return settings.GITHUB_OAUTH_REDIRECT_URI
    return request.build_absolute_uri("/api/auth/github/callback/")


def sanitize_next_url(request: HttpRequest, next_url: str | None, fallback: str) -> str:
    if next_url and url_has_allowed_host_and_scheme(
        next_url,
        allowed_hosts={request.get_host()},
        require_https=request.is_secure(),
    ):
        return next_url
    if next_url and next_url.startswith("/"):
        return next_url
    return fallback


def begin_github_login(
    request: HttpRequest,
    *,
    flow: str,
    next_url: str,
    scopes: list[str] | None = None,
) -> HttpResponseRedirect:
    state = secrets.token_urlsafe(24)
    request.session["github_oauth_state"] = state
    request.session["github_oauth_flow"] = {
        "flow": flow,
        "next_url": next_url,
    }
    query = urlencode(
        {
            "client_id": settings.GITHUB_OAUTH_CLIENT_ID,
            "redirect_uri": build_github_redirect_uri(request),
            "scope": " ".join(scopes or settings.GITHUB_OAUTH_SCOPES),
            "state": state,
        }
    )
    return redirect(f"{GITHUB_AUTHORIZE_URL}?{query}")


def exchange_code_for_token(request: HttpRequest, code: str) -> dict:
    response = requests.post(
        GITHUB_ACCESS_TOKEN_URL,
        headers={"Accept": "application/json"},
        data={
            "client_id": settings.GITHUB_OAUTH_CLIENT_ID,
            "client_secret": settings.GITHUB_OAUTH_CLIENT_SECRET,
            "code": code,
            "redirect_uri": build_github_redirect_uri(request),
        },
        timeout=10,
    )
    response.raise_for_status()
    return response.json()


def fetch_github_profile(access_token: str) -> dict:
    response = requests.get(
        f"{GITHUB_API_URL}/user",
        headers={
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {access_token}",
            "X-GitHub-Api-Version": "2022-11-28",
        },
        timeout=10,
    )
    response.raise_for_status()
    return response.json()


def fetch_github_primary_email(access_token: str) -> str:
    response = requests.get(
        f"{GITHUB_API_URL}/user/emails",
        headers={
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {access_token}",
            "X-GitHub-Api-Version": "2022-11-28",
        },
        timeout=10,
    )
    response.raise_for_status()
    emails = response.json()
    primary = next((email for email in emails if email.get("primary")), None)
    verified = next((email for email in emails if email.get("verified")), None)
    return (primary or verified or {}).get("email", "")


def upsert_github_admin_user(profile: dict, access_token: str, scope: str):
    return upsert_github_user(
        profile,
        access_token,
        scope,
        is_staff=True,
        is_superuser=(profile.get("login") or "") in settings.GITHUB_SUPERUSER_USERS,
    )


def upsert_github_user(
    profile: dict,
    access_token: str,
    scope: str,
    *,
    is_staff: bool = False,
    is_superuser: bool = False,
):
    username = profile.get("login") or ""
    User = get_user_model()
    user, _ = User.objects.get_or_create(username=username)
    user.email = profile.get("email") or user.email or ""
    user.first_name = profile.get("name") or user.first_name
    user.github_login = username
    user.github_access_token = access_token
    user.github_token_scope = scope
    user.is_active = True
    user.is_staff = is_staff
    user.is_superuser = is_superuser
    user.set_unusable_password()
    user.save()
    return user


def finish_github_login(request: HttpRequest) -> HttpResponseRedirect:
    flow_data = request.session.get("github_oauth_flow") or {}
    flow = flow_data.get("flow", "admin")
    next_url = flow_data.get("next_url") or (
        reverse("admin:index") if flow == "admin" else "/"
    )
    expected_state = request.session.get("github_oauth_state")
    state = request.GET.get("state")
    code = request.GET.get("code")
    if not expected_state or state != expected_state or not code:
        if flow == "admin":
            messages.error(request, "GitHub login could not be verified.")
            return redirect("admin:login")
        return redirect(f"{next_url}{'&' if '?' in next_url else '?'}github_auth_error=state")

    token_payload = exchange_code_for_token(request, code)
    access_token = token_payload.get("access_token", "")
    if not access_token:
        if flow == "admin":
            messages.error(request, "GitHub did not return an access token.")
            return redirect("admin:login")
        return redirect(f"{next_url}{'&' if '?' in next_url else '?'}github_auth_error=token")

    profile = fetch_github_profile(access_token)
    username = profile.get("login") or ""
    if flow == "admin" and username not in settings.GITHUB_ADMIN_USERS:
        messages.error(request, "This GitHub account is not allowed to access the admin.")
        return redirect("admin:login")

    if not profile.get("email"):
        profile["email"] = fetch_github_primary_email(access_token)

    if flow == "admin":
        user = upsert_github_admin_user(
            profile,
            access_token,
            token_payload.get("scope", ""),
        )
    else:
        user = upsert_github_user(
            profile,
            access_token,
            token_payload.get("scope", ""),
        )
    login(request, user, backend="django.contrib.auth.backends.ModelBackend")
    request.session.pop("github_oauth_state", None)
    request.session.pop("github_oauth_flow", None)
    return redirect(next_url)
