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
            return Project.objects.all()

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
        cch = cache.get("gists")
        if cch:
            return Response(data=cch)
        else:
            res = requests.request(
                HTTPMethod.GET, self.BASE + f"users/{os.getenv('GITHUB_USER')}/gists"
            )
            res.raise_for_status()
            data = res.json()
            for entry in data:
                BlogEntry.create_from_gist(entry)
            data = self.get_serializer(
                many=True, instance=self.get_queryset().all()
            ).data
            cache.set("gists", data, timeout=60 * 5)
        return Response(data=data)

    @action([HTTPMethod.GET], detail=False, url_path="gist/(?P<id>[^/.]+)")
    def get_gist(self, request: Request, id: str):
        cch = cache.get(f"gist-{id}")
        if cch:
            return Response(data=cch)
        try:
            entry = BlogEntry.objects.get(gist_id=id)
        except BlogEntry.DoesNotExist:
            url = self.BASE + f"gists/{id}"
            res = requests.request(HTTPMethod.GET, url)
            res.raise_for_status()
            data = res.json()
            entry = BlogEntry.create_from_gist(data)
        result = self.get_serializer(entry).data
        cache.set(f"gist-{id}", result, timeout=60 * 5)
        return Response(data=result)

    @action([HTTPMethod.GET], detail=False, url_path="projects")
    def list_projects(
        self,
        request: Request,
    ):
        cch = cache.get("projects")
        if cch:
            return Response(data=cch)
        else:
            response = requests.request(
                HTTPMethod.GET, self.BASE + f"users/{os.getenv('GITHUB_USER')}/repos"
            )
            response.raise_for_status()
            data = response.json()
            for repo in data:
                Project.create_from_repo(repo)
            data = self.get_serializer(
                many=True, instance=self.get_queryset().all()
            ).data
            cache.set("projects", data, 60 * 5)
            return Response(data=data)

    @action([HTTPMethod.GET], detail=False, url_path="project/(?P<id>[^/.]+)")
    def get_project(self, request: Request, id: str):
        cch = cache.get(f"project-{id}")
        if cch:
            return Response(data=cch)
        try:
            entry = Project.objects.get(github_id=id)
        except Project.DoesNotExist:
            url = self.BASE + f"repos/{os.getenv('GITHUB_USER')}/{id}"
            res = requests.request(HTTPMethod.GET, url)
            res.raise_for_status()
            data = res.json()
            entry = Project.create_from_repo(data)
        result = self.get_serializer(entry).data
        cache.set(f"project-{id}", result, timeout=60 * 5)
        return Response(data=result)
