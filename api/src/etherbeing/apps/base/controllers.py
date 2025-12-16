import os
from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response
from http import HTTPMethod
import requests
from django.core.cache import cache
from .serializers import BlogEntrySerializer, ProjectSerializer
from .models import BlogEntry, Project


class GithubViewSet(GenericViewSet):
    """
    Serves and cache the github data
    """

    BASE = "https://api.github.com/"

    def get_queryset(self):
        if self.action in [self.list_gists.__name__, self.get_gist.__name__]:
            return BlogEntry.objects.all()
        elif self.action in [self.list_projects.__name__, self.get_project.__name__]:
            return Project.objects.all().order_by("-stargazers_count")

    def get_serializer_class(self):
        if self.action in [self.list_gists.__name__, self.get_gist.__name__]:
            return BlogEntrySerializer
        elif self.action in [self.list_projects.__name__, self.get_project.__name__]:
            return ProjectSerializer
        else:
            return None

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
                if (
                    res := requests.request(
                        HTTPMethod.GET,
                        self.BASE + f"users/{os.getenv('GITHUB_USER')}/gists",
                    )
                ).ok:
                    for entry in res.json():
                        BlogEntry.create_from_gist(entry)
            except requests.exceptions.ConnectionError:
                pass
            data = self.get_serializer(
                many=True, instance=self.get_queryset().all()
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
        except BlogEntry.DoesNotExist:
            if (res := requests.request(HTTPMethod.GET, self.BASE + f"gists/{id}")).ok:
                entry = BlogEntry.create_from_gist(res.json())[0]
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
                if (
                    response := requests.request(
                        HTTPMethod.GET,
                        self.BASE + f"users/{os.getenv('GITHUB_USER')}/repos",
                    )
                ).ok:
                    for repo in response.json():
                        Project.create_from_repo(repo)
            except requests.exceptions.ConnectionError:
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
            if (
                res := requests.request(
                    HTTPMethod.GET, self.BASE + f"repos/{os.getenv('GITHUB_USER')}/{id}"
                )
            ).ok:
                entry = Project.create_from_repo(res.json())[0]
        result = self.get_serializer(entry).data
        cache.set(KEY, result, timeout=60 * 5)
        return Response(data=result)
