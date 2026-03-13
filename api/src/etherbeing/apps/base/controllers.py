import os
from http import HTTPMethod, HTTPStatus

import requests
from django.conf import settings
from django.contrib.auth import logout
from django.core.cache import cache
from django.middleware.csrf import get_token
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from .admin_auth import begin_github_login, finish_github_login, github_oauth_is_enabled, sanitize_next_url
from .serializers import (
    BlogEntryCommentSerializer,
    ConfigurationSerializer,
    GithubCommentCreateSerializer,
    GithubSessionSerializer,
    BlogEntrySerializer,
    ProjectSerializer,
    ServiceRequestCreateSerializer,
    ServiceRequestSerializer,
    ServiceSerializer,
    SiteContentSerializer,
)
from .models import BlogEntry, Configuration, Project, Service, ServiceRequest, SiteContent
from .github_api import fetch_github_json
from .seed_data import initialize_configuration, initialize_site_content


class GithubViewSet(GenericViewSet):
    """
    Serves and cache the github data
    """

    def get_queryset(self):
        if self.action in [
            self.list_gists.__name__,
            self.get_gist.__name__,
            self.get_comments_for_gist.__name__,
        ]:
            return BlogEntry.objects.all().order_by("-created_at", "-updated_at")
        elif self.action in [self.list_projects.__name__, self.get_project.__name__]:
            return Project.objects.all().order_by("-pushed_at", "-updated_at", "-created_at")

    def get_serializer_class(self):
        if self.action in [self.list_gists.__name__, self.get_gist.__name__]:
            return BlogEntrySerializer
        elif self.action in [self.list_projects.__name__, self.get_project.__name__]:
            return ProjectSerializer
        elif self.action in [self.get_comments_for_gist.__name__]:
            return BlogEntryCommentSerializer
        elif self.action == self.github_session.__name__:
            return GithubSessionSerializer
        elif self.action == self.create_comment_for_gist.__name__:
            return GithubCommentCreateSerializer
        else:
            return None

    @staticmethod
    def github_headers(access_token: str | None = None):
        headers = {
            "Accept": "application/vnd.github+json",
            "User-Agent": os.getenv("GITHUB_USER", "etherbeing-site"),
            "X-GitHub-Api-Version": "2022-11-28",
        }
        if access_token:
            headers["Authorization"] = f"Bearer {access_token}"
        return headers

    @staticmethod
    def token_has_scope(scope_value: str | None, required_scope: str) -> bool:
        scopes = {
            item.strip()
            for item in (scope_value or "").replace(" ", ",").split(",")
            if item.strip()
        }
        return required_scope in scopes

    def sync_gist_comments(self, gist_id: str, access_token: str | None = None):
        response = requests.get(
            f"https://api.github.com/gists/{gist_id}/comments",
            headers=self.github_headers(access_token),
            timeout=15,
        )
        response.raise_for_status()
        return BlogEntry.update_comments_from_github(gist_id, response.json())

    def serialize_github_user(self, request: Request):
        user = request.user
        payload = {
            "is_authenticated": bool(user and user.is_authenticated),
            "csrf_token": get_token(request._request),
        }
        if user and user.is_authenticated:
            payload.update(
                {
                    "username": user.username,
                    "email": user.email,
                    "github_login": getattr(user, "github_login", ""),
                    "avatar_url": (
                        f"https://github.com/{user.github_login}.png"
                        if getattr(user, "github_login", "")
                        else ""
                    ),
                    "can_comment_on_gists": self.token_has_scope(
                        getattr(user, "github_token_scope", ""),
                        "gist",
                    ),
                }
            )
        return payload

    @action([HTTPMethod.GET], detail=False, url_path="auth/github/login")
    def github_login(self, request: Request):
        if not github_oauth_is_enabled():
            return Response(
                {"detail": "GitHub OAuth is not configured."},
                status=HTTPStatus.SERVICE_UNAVAILABLE,
            )
        next_url = sanitize_next_url(request._request, request.query_params.get("next"), "/")
        intent = request.query_params.get("intent")
        scopes = (
            settings.GITHUB_COMMENT_OAUTH_SCOPES
            if intent == "comment"
            else settings.GITHUB_FRONTEND_OAUTH_SCOPES
        )
        return begin_github_login(
            request._request,
            flow="frontend",
            next_url=next_url,
            scopes=scopes,
        )

    @action([HTTPMethod.GET], detail=False, url_path="auth/github/callback")
    def github_callback(self, request: Request):
        return finish_github_login(request._request)

    @action([HTTPMethod.GET], detail=False, url_path="auth/github/session")
    def github_session(self, request: Request):
        return Response(self.serialize_github_user(request))

    @action([HTTPMethod.POST], detail=False, url_path="auth/logout")
    def logout_view(self, request: Request):
        logout(request._request)
        return Response(self.serialize_github_user(request))

    @action([HTTPMethod.GET], detail=False, url_path="gists")
    def list_gists(
        self,
        request: Request,
    ):
        """List all gists"""
        KEY = "gists"
        if cch := cache.get(KEY):
            return Response(data=cch)
        else:
            try:
                for entry in fetch_github_json(
                    f"users/{os.getenv('GITHUB_USER')}/gists",
                    "github-user-gists",
                ):
                    BlogEntry.create_from_gist(entry)
            except requests.exceptions.RequestException:
                pass
            data = self.get_serializer(
                many=True, instance=self.get_queryset().all().order_by("-created_at")
            ).data
            cache.set(KEY, data, timeout=60 * 5)
        return Response(data=data)

    @action([HTTPMethod.GET], detail=False, url_path="gist/(?P<id>[^/.]+)")
    def get_gist(self, request: Request, id: str):
        KEY = f"gist-{id}"
        if cch := cache.get(KEY):
            return Response(data=cch)
        try:
            entry = BlogEntry.objects.get(gist_id=id)
            if not entry.content:
                gist_data = fetch_github_json(f"gists/{id}", f"github-gist-{id}")
                entry = BlogEntry.create_from_gist(gist_data)[0]
        except (BlogEntry.DoesNotExist, requests.exceptions.RequestException):
            gist_data = fetch_github_json(f"gists/{id}", f"github-gist-{id}")
            entry = BlogEntry.create_from_gist(gist_data)[0]
        result = self.get_serializer(entry).data
        cache.set(KEY, result, timeout=60 * 5)
        return Response(data=result)

    @action([HTTPMethod.GET], detail=False, url_path="projects")
    def list_projects(
        self,
        request: Request,
    ):
        KEY = "projects"
        if cch := cache.get(KEY):
            return Response(data=cch)
        else:
            try:
                repos = fetch_github_json(
                    f"users/{os.getenv('GITHUB_USER')}/repos?type=public&sort=updated&per_page=100",
                    "github-user-projects",
                )
                for repo in repos:
                    languages = fetch_github_json(
                        repo["languages_url"],
                        f"github-project-languages-{repo['id']}",
                    )
                    Project.create_from_repo(repo, languages)
            except requests.exceptions.RequestException:
                pass
            data = self.get_serializer(
                many=True, instance=self.get_queryset().all()
            ).data
            cache.set(KEY, data, 60 * 5)
            return Response(data=data)

    @action([HTTPMethod.GET], detail=False, url_path="project/(?P<id>[^/.]+)")
    def get_project(self, request: Request, id: str):
        KEY = f"project-{id}"
        if cch := cache.get(KEY):
            return Response(data=cch)
        try:
            entry = Project.objects.get(github_id=id)
        except Project.DoesNotExist:
            project = fetch_github_json(
                f"repositories/{id}",
                f"github-project-{id}",
            )
            entry = Project.create_from_repo(project)[0]
        result = self.get_serializer(entry).data
        cache.set(KEY, result, timeout=60 * 5)
        return Response(data=result)

    @action([HTTPMethod.GET], detail=True, url_path="comments")
    def get_comments_for_gist(self, request: Request, pk: str):
        KEY = f"comments-{pk}"
        if cch := cache.get(KEY):
            return Response(data=cch)

        try:
            access_token = (
                getattr(request.user, "github_access_token", "")
                if request.user.is_authenticated
                else None
            )
            comments = self.sync_gist_comments(pk, access_token or None)
        except requests.exceptions.RequestException:
            try:  # if connection error then just give him back what's on the DB
                comments = BlogEntry.objects.get(gist_id=pk).comments.all()
            except BlogEntry.DoesNotExist:
                return Response(status=HTTPStatus.BAD_GATEWAY)
        result = self.get_serializer(comments, many=True).data
        cache.set(KEY, result, timeout=60 * 5)
        return Response(data=result)

    @action([HTTPMethod.GET, HTTPMethod.POST], detail=False, url_path="gist/(?P<id>[^/.]+)/comments")
    def create_comment_for_gist(self, request: Request, id: str):
        if request.method == HTTPMethod.GET:
            comments = self.sync_gist_comments(
                id,
                getattr(request.user, "github_access_token", "") or None,
            )
            result = BlogEntryCommentSerializer(comments, many=True).data
            cache.set(f"comments-{id}", result, timeout=60 * 5)
            return Response(result)

        if not request.user.is_authenticated or not getattr(request.user, "github_access_token", ""):
            return Response(
                {"detail": "GitHub login is required to comment."},
                status=HTTPStatus.UNAUTHORIZED,
            )
        if not self.token_has_scope(getattr(request.user, "github_token_scope", ""), "gist"):
            return Response(
                {"detail": "GitHub gist permission is required to comment."},
                status=HTTPStatus.FORBIDDEN,
            )

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        response = requests.post(
            f"https://api.github.com/gists/{id}/comments",
            headers=self.github_headers(request.user.github_access_token),
            json={"body": serializer.validated_data["content"]},
            timeout=15,
        )
        response.raise_for_status()
        comments = self.sync_gist_comments(id, request.user.github_access_token)
        created = next(
            (
                comment
                for comment in comments
                if comment.github_id == str(response.json().get("id", ""))
            ),
            comments[-1] if comments else None,
        )
        cache.delete(f"comments-{id}")
        if created is None:
            return Response(status=HTTPStatus.BAD_GATEWAY)
        return Response(BlogEntryCommentSerializer(created).data, status=HTTPStatus.CREATED)


class SiteContentViewSet(GenericViewSet):
    serializer_class = SiteContentSerializer

    def get_serializer_class(self):
        if self.action == self.service.__name__:
            return ServiceSerializer
        if self.action == self.request_service.__name__:
            if self.request.method == HTTPMethod.POST:
                return ServiceRequestCreateSerializer
            return ServiceRequestSerializer
        return super().get_serializer_class()

    @staticmethod
    def normalize_site_content_payload(payload: dict):
        payload["strategy_business_idea"] = {
            "blog_integrations": [],
            "content_to_publish": [],
            "other_services": [],
            **(payload.get("strategy_business_idea") or {}),
        }
        return payload

    @action([HTTPMethod.GET], detail=False, url_path="content")
    def content(self, request: Request):
        KEY = "site-content"
        if cached := cache.get(KEY):
            return Response(data=self.normalize_site_content_payload(cached))

        site_content = (
            SiteContent.objects.prefetch_related(
                "about_highlights",
                "skills",
                "services",
                "contact_groups__links",
            )
            .filter(slug="primary")
            .first()
        )
        if site_content is None:
            site_content = initialize_site_content()

        data = self.normalize_site_content_payload(self.get_serializer(site_content).data)
        cache.set(KEY, data, timeout=60 * 5)
        return Response(data=data)

    @action([HTTPMethod.GET], detail=False, url_path="configuration")
    def configuration(self, request: Request):
        key = "site-configuration"
        if cached := cache.get(key):
            return Response(data=cached)

        configuration = Configuration.objects.filter(slug="primary").first()
        if configuration is None:
            configuration = initialize_configuration()

        data = ConfigurationSerializer(configuration).data
        cache.set(key, data, timeout=60 * 5)
        return Response(data=data)

    @action([HTTPMethod.GET], detail=False, url_path=r"service/(?P<slug>[-\w]+)")
    def service(self, request: Request, slug: str):
        key = f"service-{slug}"
        if cached := cache.get(key):
            return Response(data=cached)

        service = Service.objects.filter(slug=slug).first()
        if service is None:
            initialize_site_content()
            service = Service.objects.filter(slug=slug).first()
        if service is None:
            return Response({"detail": "Service not found."}, status=HTTPStatus.NOT_FOUND)

        data = ServiceSerializer(service).data
        cache.set(key, data, timeout=60 * 5)
        return Response(data=data)

    @action(
        [HTTPMethod.POST],
        detail=False,
        url_path=r"service/(?P<slug>[-\w]+)/request",
    )
    def request_service(self, request: Request, slug: str):
        service = Service.objects.filter(slug=slug).first()
        if service is None:
            return Response({"detail": "Service not found."}, status=HTTPStatus.NOT_FOUND)
        if not request.user.is_authenticated:
            return Response(
                {"detail": "Authentication is required to request a service."},
                status=HTTPStatus.UNAUTHORIZED,
            )

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        service_request = ServiceRequest.objects.create(
            service=service,
            requester=request.user,
            message=serializer.validated_data.get("message", ""),
        )
        cache.delete(f"service-{slug}")
        return Response(
            ServiceRequestSerializer(service_request).data,
            status=HTTPStatus.CREATED,
        )
