from typing import Any
from django.db import models
from django.contrib.auth.models import AbstractUser as BaseUser
# Create your models here.


class User(BaseUser):
    pass


class BlogEntry(models.Model):
    id = models.AutoField(primary_key=True)
    gist_id = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    content = models.TextField(default=None)

    @classmethod
    def create_from_gist(cls, gist: dict[str, Any]):
        content = gist.get("files", {}).get("content.md", {}).get("content", None)
        if not content:
            return None
        entry = cls.objects.get_or_create(
            gist_id=gist["id"],
            defaults={
                "created_at": gist["created_at"],
                "updated_at": gist["updated_at"],
                "content": content,
            },
        )[0]
        return entry

    def __str__(self):
        return self.title


class Project(models.Model):
    github_id = models.CharField(unique=True, default=None)
    description = models.CharField(default=None, null=True, blank=True)
    stargazers_count = models.IntegerField(default=None)
    watchers_count = models.IntegerField(default=None)
    name = models.CharField(default=None, max_length=50)

    @classmethod
    def create_from_repo(cls, repo: dict[str, Any]):
        cls.objects.get_or_create(
            github_id=repo["id"],
            defaults={
                "name": repo["name"],
                "description": repo["description"],
                "stargazers_count": repo["stargazers_count"],
                "watchers_count": repo["watchers_count"],
            },
        )
