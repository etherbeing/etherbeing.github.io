from typing import Any, Generator
from django.db import models
from django.contrib.auth.models import AbstractUser as BaseUser
from django.utils.timezone import datetime
# Create your models here.


class User(BaseUser):
    pass


class BlogEntryComment(models.Model):
    github_id = models.CharField(default=None)
    username = models.CharField(default=None)
    content = models.CharField(default=None)
    date = models.DateField(default=None)

    def __str__(self):
        return self.github_id


class BlogEntry(models.Model):
    id = models.AutoField(primary_key=True)
    gist_id = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(default=None, null=True)
    updated_at = models.DateTimeField(default=None, null=True)
    description = models.TextField(default=None, null=True, blank=True)
    content = models.TextField(default=None)
    html_url = models.URLField(default=None, null=True)
    comments = models.ManyToManyField(
        BlogEntryComment,
    )

    @classmethod
    def create_from_gist(cls, gist: dict[str, Any]):
        content = gist.get("files", {}).get("content.md", {}).get("content", None)
        if not content:
            return None
        return cls.objects.update_or_create(
            gist_id=gist["id"],
            defaults={
                "created_at": gist["created_at"],
                "updated_at": gist["updated_at"],
                "description": gist["description"],
                "html_url": gist["html_url"],
                "content": content,
            },
        )

    @classmethod
    def update_comments_from_github(cls, github_data: list[dict[str, Any]]):
        def _to_gen() -> Generator[BlogEntryComment]:
            for comment in github_data:  # I don't know what to do yet with the response from github at this point
                yield BlogEntryComment()

        return BlogEntryComment.objects.bulk_create(
            _to_gen(), update_conflicts=True
        )  # update or create for bulk

    def __str__(self):
        return self.gist_id


class Project(models.Model):
    github_id = models.CharField(unique=True, default=None)
    description = models.CharField(default=None, null=True, blank=True)
    stargazers_count = models.IntegerField(default=None)
    watchers_count = models.IntegerField(default=None)
    name = models.CharField(default=None, max_length=50)
    created_at = models.DateField(default=None, null=True)
    updated_at = models.DateField(default=None, null=True)
    pushed_at = models.DateField(default=None, null=True)
    html_url = models.URLField(default=None, null=True, blank=True)
    language = models.CharField(default=None, null=True, blank=True, max_length=50)

    @classmethod
    def create_from_repo(cls, repo: dict[str, Any]):
        return cls.objects.update_or_create(
            github_id=repo["id"],
            defaults={
                "name": repo["name"],
                "description": repo["description"],
                "stargazers_count": repo["stargazers_count"],
                "watchers_count": repo["watchers_count"],
                "created_at": datetime.fromisoformat(repo["created_at"]),
                "updated_at": datetime.fromisoformat(repo["updated_at"]),
                "pushed_at": datetime.fromisoformat(repo["pushed_at"]),
                "html_url": repo["html_url"],
                "language": repo["language"],
            },
        )
