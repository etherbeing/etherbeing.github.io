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
    class Category(models.TextChoices):
        CYBERSECURITY = "cybersecurity", "Cybersecurity"
        SOFTWARE_DEVELOPMENT = "software-development", "Software Development"
        DEVOPS = "devops", "DevOps"
        PHILOSOPHY = "philosophy", "Philosophy"
        POLITICS = "politics", "Politics"
        PROJECT_ADS = "project-ads", "Project Ads"
        ARTIFICIAL_INTELLIGENCE = "artificial-intelligence", "Artificial Intelligence"
        RESEARCHES = "researches", "Researches"

    id = models.AutoField(primary_key=True)
    gist_id = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(default=None, null=True)
    updated_at = models.DateTimeField(default=None, null=True)
    description = models.TextField(default=None, null=True, blank=True)
    content = models.TextField(default="")
    html_url = models.URLField(default=None, null=True)
    image_url = models.CharField(max_length=500, default="", blank=True)
    hide_from_web = models.BooleanField(default=False)
    category = models.CharField(
        max_length=64,
        choices=Category.choices,
        default=Category.SOFTWARE_DEVELOPMENT,
    )
    social_networks = models.JSONField(default=list, blank=True)
    comments = models.ManyToManyField(
        BlogEntryComment,
        blank=True,
    )

    @classmethod
    def create_from_gist(cls, gist: dict[str, Any]):
        content = cls.extract_content_from_gist(gist)
        image_url = cls.extract_image_from_gist(gist)
        metadata = cls.extract_metadata_from_gist(gist)
        return cls.objects.update_or_create(
            gist_id=gist["id"],
            defaults={
                "created_at": gist["created_at"],
                "updated_at": gist["updated_at"],
                "description": gist["description"],
                "html_url": gist["html_url"],
                "content": content or "",
                "image_url": image_url or "",
                "category": metadata.get("category") or cls.Category.SOFTWARE_DEVELOPMENT,
                "social_networks": metadata.get("social_networks") or [],
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
        if preferred := files.get("image.png"):
            if preferred.get("raw_url"):
                return preferred["raw_url"]

        for file_data in files.values():
            filename = (file_data.get("filename") or "").lower()
            file_type = (file_data.get("type") or "").lower()
            language = (file_data.get("language") or "").lower()
            is_image_name = filename.endswith(
                (".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg", ".avif")
            )
            is_image_type = file_type.startswith("image/")
            if (is_image_name or is_image_type or language == "image") and file_data.get("raw_url"):
                return file_data["raw_url"]
        return None

    @staticmethod
    def extract_metadata_from_gist(gist: dict[str, Any]) -> dict[str, Any]:
        files = gist.get("files", {})
        metadata_file = files.get("metadata.json")
        if not metadata_file or not metadata_file.get("content"):
            return {}
        try:
            import json

            payload = json.loads(metadata_file["content"])
        except (TypeError, ValueError):
            return {}
        return payload if isinstance(payload, dict) else {}

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


class PublishedPost(models.Model):
    title = models.CharField(max_length=255)
    category = models.CharField(max_length=64, choices=BlogEntry.Category.choices)
    social_networks = models.JSONField(default=list, blank=True)
    gist_id = models.CharField(max_length=255, blank=True, default="")
    gist_url = models.URLField(blank=True, default="")
    content = models.TextField(default="")
    excerpt = models.TextField(blank=True, default="")
    notification_results = models.JSONField(default=dict, blank=True)
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="published_posts",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at", "-id"]

    def __str__(self):
        return self.title


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
    featured_chart_symbol = models.CharField(max_length=64, default="BITSTAMP:ETHUSD")
    featured_chart_title = models.CharField(max_length=255, default="Ethereum")
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
    image_url = models.CharField(max_length=500, default="", blank=True)
    headline = models.CharField(max_length=255, default="", blank=True)
    description = models.TextField(default="", blank=True)
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
    slug = models.SlugField(max_length=255, unique=True, default="")
    title = models.CharField(max_length=255)
    headline = models.CharField(max_length=255, default="", blank=True)
    starting_price = models.PositiveIntegerField()
    description = models.TextField()
    overview = models.TextField(default="", blank=True)
    skills = models.JSONField(default=list, blank=True)
    deliverables = models.JSONField(default=list, blank=True)
    process_steps = models.JSONField(default=list, blank=True)
    outcomes = models.JSONField(default=list, blank=True)
    engagement_cta = models.CharField(max_length=255, default="", blank=True)
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["sort_order", "id"]

    def __str__(self):
        return self.title


class ServiceRequest(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        REVIEWING = "reviewing", "Reviewing"
        CONTACTED = "contacted", "Contacted"
        DELIVERED = "delivered", "Delivered"
        CANCELLED = "cancelled", "Cancelled"

    service = models.ForeignKey(
        Service,
        on_delete=models.CASCADE,
        related_name="requests",
    )
    requester = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="service_requests",
    )
    status = models.CharField(
        max_length=32,
        choices=Status.choices,
        default=Status.PENDING,
    )
    message = models.TextField(default="", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at", "-id"]

    def __str__(self):
        return f"{self.service.title} / {self.requester.username}"


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


class GalleryPhoto(models.Model):
    site_content = models.ForeignKey(
        SiteContent,
        on_delete=models.CASCADE,
        related_name="gallery_photos",
    )
    title = models.CharField(max_length=255)
    image_url = models.CharField(max_length=500)
    caption = models.TextField(default="", blank=True)
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["sort_order", "id"]

    def __str__(self):
        return self.title


class ContactThread(models.Model):
    class Status(models.TextChoices):
        OPEN = "open", "Open"
        REPLIED = "replied", "Replied"
        CLOSED = "closed", "Closed"

    requester = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="contact_threads",
    )
    subject = models.CharField(max_length=255)
    status = models.CharField(max_length=32, choices=Status.choices, default=Status.OPEN)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_message_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-last_message_at", "-id"]

    def __str__(self):
        return f"{self.requester.username}: {self.subject}"


class ContactMessage(models.Model):
    thread = models.ForeignKey(
        ContactThread,
        on_delete=models.CASCADE,
        related_name="messages",
    )
    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="contact_messages",
    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at", "id"]

    @property
    def is_staff_reply(self) -> bool:
        return bool(self.sender and self.sender.is_staff)

    def __str__(self):
        return f"{self.sender.username} -> {self.thread.subject}"
