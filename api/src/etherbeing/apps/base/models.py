from typing import Any

from django.contrib.auth.models import AbstractUser as BaseUser
from django.db import models
from django.utils.dateparse import parse_datetime


class User(BaseUser):
    github_login = models.CharField(max_length=255, blank=True, default="")
    github_access_token = models.TextField(blank=True, default="")
    github_token_scope = models.CharField(max_length=255, blank=True, default="")


class Configuration(models.Model):
    slug = models.SlugField(default="primary", unique=True)
    site_name = models.CharField(max_length=255, default="etherbeing")
    short_name = models.CharField(max_length=64, default="etherbeing")
    site_description = models.TextField(default="Cybersecurity, Rust engineering, and research.")
    favicon_url = models.URLField(
        default="https://etherbeing.github.io/favicon.png",
        blank=True,
    )
    theme_color = models.CharField(max_length=20, default="#020617")
    background_color = models.CharField(max_length=20, default="#020617")

    @classmethod
    def get_solo(cls):
        configuration, _ = cls.objects.get_or_create(slug="primary")
        return configuration

    def __str__(self):
        return self.site_name


class BlogEntryComment(models.Model):
    github_id = models.CharField(max_length=255, default="")
    username = models.CharField(max_length=255, default="")
    content = models.TextField(default="")
    date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.github_id


class BlogEntry(models.Model):
    id = models.AutoField(primary_key=True)
    gist_id = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(default=None, null=True)
    updated_at = models.DateTimeField(default=None, null=True)
    description = models.TextField(default=None, null=True, blank=True)
    content = models.TextField(default="")
    html_url = models.URLField(default=None, null=True)
    image_url = models.CharField(max_length=500, default="", blank=True)
    comments = models.ManyToManyField(
        BlogEntryComment,
        blank=True,
    )

    @classmethod
    def create_from_gist(cls, gist: dict[str, Any]):
        content = cls.extract_content_from_gist(gist)
        image_url = cls.extract_image_from_gist(gist)
        return cls.objects.update_or_create(
            gist_id=gist["id"],
            defaults={
                "created_at": gist["created_at"],
                "updated_at": gist["updated_at"],
                "description": gist["description"],
                "html_url": gist["html_url"],
                "content": content or "",
                "image_url": image_url or "",
            },
        )

    @staticmethod
    def extract_content_from_gist(gist: dict[str, Any]) -> str | None:
        files = gist.get("files", {})
        preferred_names = ["content.md", "README.md", "readme.md", "index.md"]
        for filename in preferred_names:
            file_data = files.get(filename)
            if file_data and file_data.get("content"):
                return file_data["content"]

        for file_data in files.values():
            language = (file_data.get("language") or "").lower()
            filename = (file_data.get("filename") or "").lower()
            if file_data.get("content") and (
                language in {"markdown", "md"} or filename.endswith((".md", ".mdx", ".txt"))
            ):
                return file_data["content"]

        for file_data in files.values():
            if file_data.get("content"):
                return file_data["content"]
        return None

    @staticmethod
    def extract_image_from_gist(gist: dict[str, Any]) -> str | None:
        files = gist.get("files", {})
        image_file = files.get("image.png")
        if image_file and image_file.get("raw_url"):
            return image_file["raw_url"]
        return None

    @classmethod
    def update_comments_from_github(
        cls,
        gist_id: str,
        github_data: list[dict[str, Any]],
    ) -> list[BlogEntryComment]:
        entry, _ = cls.objects.get_or_create(gist_id=gist_id, defaults={"content": ""})
        comments: list[BlogEntryComment] = []
        comment_ids: list[int] = []
        for comment in github_data:
            comment_date = parse_datetime(comment.get("created_at", ""))
            github_id = str(comment.get("id", ""))
            existing = BlogEntryComment.objects.filter(github_id=github_id).first()
            if existing is None:
                existing = BlogEntryComment(github_id=github_id)
            existing.username = (comment.get("user") or {}).get("login", "")
            existing.content = comment.get("body", "")
            existing.date = comment_date.date() if comment_date else None
            existing.save()
            comments.append(existing)
            comment_ids.append(existing.pk)

        if comment_ids:
            entry.comments.set(comment_ids)
        else:
            entry.comments.clear()
        return comments

    def __str__(self):
        return self.gist_id


class Project(models.Model):
    github_id = models.CharField(max_length=255, unique=True, default="")
    description = models.TextField(default=None, null=True, blank=True)
    stargazers_count = models.IntegerField(default=0)
    watchers_count = models.IntegerField(default=0)
    name = models.CharField(default="", max_length=255)
    created_at = models.DateField(default=None, null=True)
    updated_at = models.DateField(default=None, null=True)
    pushed_at = models.DateField(default=None, null=True)
    html_url = models.URLField(default=None, null=True, blank=True)
    language = models.CharField(default=None, null=True, blank=True, max_length=50)
    languages = models.JSONField(default=list, blank=True)

    @classmethod
    def create_from_repo(cls, repo: dict[str, Any], languages: dict[str, int] | None = None):
        created_at = parse_datetime(repo["created_at"])
        updated_at = parse_datetime(repo["updated_at"])
        pushed_at = parse_datetime(repo["pushed_at"])
        language_names = cls.to_language_list(languages, repo.get("language"))
        return cls.objects.update_or_create(
            github_id=str(repo["id"]),
            defaults={
                "name": repo["name"],
                "description": repo["description"],
                "stargazers_count": repo["stargazers_count"],
                "watchers_count": repo["watchers_count"],
                "created_at": created_at.date() if created_at else None,
                "updated_at": updated_at.date() if updated_at else None,
                "pushed_at": pushed_at.date() if pushed_at else None,
                "html_url": repo["html_url"],
                "language": repo.get("language") or (language_names[0] if language_names else None),
                "languages": language_names,
            },
        )

    @staticmethod
    def to_language_list(
        languages: dict[str, int] | None, primary_language: str | None = None
    ) -> list[str]:
        ordered = sorted(
            (languages or {}).items(),
            key=lambda item: item[1],
            reverse=True,
        )
        names = [name for name, _ in ordered]
        if primary_language and primary_language not in names:
            names.insert(0, primary_language)
        elif primary_language and names and names[0] != primary_language:
            names.remove(primary_language)
            names.insert(0, primary_language)
        return names

    def __str__(self):
        return self.name


class SiteContent(models.Model):
    slug = models.SlugField(default="primary", unique=True)
    site_title = models.CharField(max_length=255)
    hero_titles = models.JSONField(default=list, blank=True)
    hero_summary = models.TextField()
    hero_cta_label = models.CharField(max_length=255, default="Download CV")
    hero_cta_url = models.CharField(max_length=255, default="/cv.pdf")
    about_short_bio = models.TextField()
    buy_me_a_coffee_url = models.URLField(blank=True)
    contact_intro = models.TextField()
    footer_copy = models.CharField(max_length=255)
    footer_tagline = models.CharField(max_length=255)
    strategy_business_idea = models.JSONField(default=dict, blank=True)

    def __str__(self):
        return self.site_title


class AboutHighlight(models.Model):
    class Column(models.TextChoices):
        LEFT = "left", "Left"
        RIGHT = "right", "Right"

    site_content = models.ForeignKey(
        SiteContent,
        on_delete=models.CASCADE,
        related_name="about_highlights",
    )
    title = models.CharField(max_length=255)
    content = models.TextField()
    column = models.CharField(max_length=16, choices=Column.choices)
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["sort_order", "id"]

    def __str__(self):
        return self.title


class Skill(models.Model):
    site_content = models.ForeignKey(
        SiteContent,
        on_delete=models.CASCADE,
        related_name="skills",
    )
    name = models.CharField(max_length=255)
    image_key = models.CharField(max_length=50)
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["sort_order", "id"]

    def __str__(self):
        return self.name


class Service(models.Model):
    site_content = models.ForeignKey(
        SiteContent,
        on_delete=models.CASCADE,
        related_name="services",
    )
    title = models.CharField(max_length=255)
    starting_price = models.PositiveIntegerField()
    description = models.TextField()
    skills = models.JSONField(default=list, blank=True)
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["sort_order", "id"]

    def __str__(self):
        return self.title


class ContactGroup(models.Model):
    site_content = models.ForeignKey(
        SiteContent,
        on_delete=models.CASCADE,
        related_name="contact_groups",
    )
    title = models.CharField(max_length=255)
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["sort_order", "id"]

    def __str__(self):
        return self.title


class ContactLink(models.Model):
    group = models.ForeignKey(
        ContactGroup,
        on_delete=models.CASCADE,
        related_name="links",
    )
    label = models.CharField(max_length=255)
    url = models.CharField(max_length=500)
    icon = models.CharField(max_length=50, blank=True)
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["sort_order", "id"]

    def __str__(self):
        return self.label
