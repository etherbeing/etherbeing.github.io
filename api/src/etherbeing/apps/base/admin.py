import os

from django.conf import settings
from django.contrib import admin, messages
from django.contrib.auth import get_user_model
from django.http import HttpRequest
from django.utils import timezone
from django.shortcuts import redirect, render
from django.urls import path, reverse

from .admin_auth import (
    begin_github_login,
    finish_github_login,
    github_oauth_is_enabled,
    recaptcha_is_enabled,
    sanitize_next_url,
    verify_recaptcha_token,
)
from .forms import BootstrapSuperuserForm, PublishBlogPostForm, RecaptchaAdminAuthenticationForm
from .models import (
    AboutHighlight,
    BlogEntry,
    BlogEntryComment,
    Configuration,
    ContactMessage,
    ContactGroup,
    ContactLink,
    ContactThread,
    GalleryPhoto,
    Project,
    PublishedPost,
    Service,
    ServiceRequest,
    SiteContent,
    Skill,
    User,
)
from .publishing import publish_gist_post
from .seed_data import initialize_site_content


class EtherbeingAdminSite(admin.AdminSite):
    site_header = "etherbeing administration"
    site_title = "etherbeing admin"
    index_title = "Content operations"
    login_form = RecaptchaAdminAuthenticationForm
    login_template = "admin/etherbeing_login.html"

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path("github/login/", self.github_login, name="github-login"),
            path("github/callback/", self.github_callback, name="github-callback"),
            path("bootstrap-superuser/", self.bootstrap_superuser, name="bootstrap-superuser"),
            path("publishing/blog-posts/new/", self.admin_view(self.publish_blog_post), name="publish-blog-post"),
        ]
        return custom_urls + urls

    def each_context(self, request):
        context = super().each_context(request)
        configuration = Configuration.get_solo()
        github_publish_ready = bool(
            getattr(request.user, "github_access_token", "")
            or os.getenv("GITHUB_PUBLISH_ACCESS_TOKEN", "")
        )
        publishing_channels = [
            {
                "key": "github",
                "label": "GitHub publishing token",
                "state": "ready" if github_publish_ready else "missing",
                "detail": "Required to create the backing gist for a post.",
            },
            {
                "key": "telegram",
                "label": "Telegram delivery",
                "state": "ready" if os.getenv("TELEGRAM_TOKEN", "") and os.getenv("TELEGRAM_TO", "") else "missing",
                "detail": "Uses TELEGRAM_TOKEN and TELEGRAM_TO.",
            },
            {
                "key": "discord",
                "label": "Discord delivery",
                "state": "ready" if os.getenv("DISCORD_WEBHOOK", "") else "missing",
                "detail": "Uses the configured Discord webhook.",
            },
            {
                "key": "whatsapp",
                "label": "WhatsApp delivery",
                "state": (
                    "ready"
                    if all(
                        [
                            os.getenv("EVOLUTION_API_BASE_URL", ""),
                            os.getenv("EVOLUTION_API_INSTANCE", ""),
                            os.getenv("EVOLUTION_API_TOKEN", ""),
                            os.getenv("EVOLUTION_API_CHAT_ID", ""),
                        ]
                    )
                    else "missing"
                ),
                "detail": "Uses Evolution API base URL, instance, token, and chat id.",
            },
        ]
        context.update(
            {
                "admin_favicon_url": configuration.favicon_url,
                "admin_site_name": configuration.site_name,
                "publish_blog_post_url": reverse("admin:publish-blog-post"),
                "publishing_channels": publishing_channels,
                "publishing_ready_count": sum(1 for channel in publishing_channels if channel["state"] == "ready"),
            }
        )
        return context

    @staticmethod
    def can_bootstrap_superuser() -> bool:
        return settings.DEBUG and not get_user_model().objects.filter(is_superuser=True).exists()

    def login(self, request, extra_context=None):
        configuration = Configuration.get_solo()
        extra_context = {
            **(extra_context or {}),
            "github_login_enabled": github_oauth_is_enabled(),
            "github_login_url": reverse("admin:github-login"),
            "recaptcha_enabled": recaptcha_is_enabled(),
            "recaptcha_site_key": settings.RECAPTCHA_SITE_KEY,
            "show_bootstrap_superuser": self.can_bootstrap_superuser(),
            "bootstrap_superuser_url": reverse("admin:bootstrap-superuser"),
            "bootstrap_superuser_form": BootstrapSuperuserForm(),
            "admin_favicon_url": configuration.favicon_url,
            "admin_site_name": configuration.site_name,
        }
        return super().login(request, extra_context=extra_context)

    def github_login(self, request: HttpRequest):
        if not github_oauth_is_enabled():
            messages.error(request, "GitHub OAuth is not configured.")
            return redirect("admin:login")
        if recaptcha_is_enabled():
            result = verify_recaptcha_token(
                request.GET.get("recaptcha_token", ""),
                action="admin_login",
                remoteip=request.META.get("REMOTE_ADDR"),
            )
            if not result.success:
                messages.error(request, "reCAPTCHA verification failed. Please try again.")
                return redirect("admin:login")
        return begin_github_login(
            request,
            flow="admin",
            next_url=sanitize_next_url(request, request.GET.get("next"), reverse("admin:index")),
            scopes=settings.GITHUB_OAUTH_SCOPES,
        )

    def github_callback(self, request: HttpRequest):
        return finish_github_login(request)

    def bootstrap_superuser(self, request: HttpRequest):
        if not self.can_bootstrap_superuser():
            messages.error(request, "Bootstrap superuser creation is not available.")
            return redirect("admin:login")
        if request.method != "POST":
            return redirect("admin:login")

        form = BootstrapSuperuserForm(request.POST)
        if not form.is_valid():
            for field_errors in form.errors.values():
                for error in field_errors:
                    messages.error(request, error)
            return redirect("admin:login")

        form.save()
        initialize_site_content()
        messages.success(request, "Superuser created successfully. You can log in now.")
        return redirect("admin:login")

    def publish_blog_post(self, request: HttpRequest):
        if request.method == "POST":
            form = PublishBlogPostForm(request.POST)
            if form.is_valid():
                result = publish_gist_post(
                    user=request.user,
                    title=form.cleaned_data["title"],
                    content=form.cleaned_data["content"],
                    category=form.cleaned_data["category"],
                    social_networks=form.cleaned_data["social_networks"],
                )
                PublishedPost.objects.create(
                    title=form.cleaned_data["title"],
                    category=form.cleaned_data["category"],
                    social_networks=form.cleaned_data["social_networks"],
                    gist_id=result.gist_id,
                    gist_url=result.html_url,
                    content=form.cleaned_data["content"],
                    excerpt=form.cleaned_data["excerpt"],
                    notification_results=result.social_results,
                    created_by=request.user if request.user.is_authenticated else None,
                )
                messages.success(request, "Blog post published successfully.")
                return redirect("admin:base_publishedpost_changelist")
        else:
            form = PublishBlogPostForm()

        context = {
            **self.each_context(request),
            "title": "Publish blog post",
            "form": form,
            "opts": BlogEntry._meta,
            "media": form.media,
        }
        return render(request, "admin/publish_blog_post.html", context)


admin_site = EtherbeingAdminSite(name="admin")


@admin.register(User, site=admin_site)
class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "email", "github_login", "is_staff", "is_superuser")
    list_filter = ("is_staff", "is_superuser", "is_active")
    search_fields = ("username", "email", "github_login")


@admin.register(Configuration, site=admin_site)
class ConfigurationAdmin(admin.ModelAdmin):
    list_display = ("site_name", "short_name", "favicon_url", "theme_color")
    search_fields = ("site_name", "short_name", "favicon_url")

    def has_add_permission(self, request):
        return not Configuration.objects.exists()


@admin.register(BlogEntry, site=admin_site)
class BlogEntryAdmin(admin.ModelAdmin):
    list_display = ("gist_id", "description", "hide_from_web", "created_at", "updated_at")
    list_filter = ("hide_from_web", "category")
    search_fields = ("gist_id", "description", "content")


@admin.register(BlogEntryComment, site=admin_site)
class BlogEntryCommentAdmin(admin.ModelAdmin):
    list_display = ("github_id", "username", "date")
    search_fields = ("github_id", "username", "content")


@admin.register(PublishedPost, site=admin_site)
class PublishedPostAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "gist_id", "created_by", "created_at")
    list_filter = ("category",)
    search_fields = ("title", "gist_id", "gist_url", "content", "excerpt")


@admin.register(Project, site=admin_site)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("name", "language", "stargazers_count", "watchers_count", "pushed_at")
    list_filter = ("language",)
    search_fields = ("name", "description", "github_id")


@admin.register(SiteContent, site=admin_site)
class SiteContentAdmin(admin.ModelAdmin):
    list_display = ("site_title", "slug", "hero_cta_label")
    search_fields = ("site_title", "slug")


@admin.register(AboutHighlight, site=admin_site)
class AboutHighlightAdmin(admin.ModelAdmin):
    list_display = ("title", "column", "sort_order")
    list_filter = ("column",)
    search_fields = ("title", "content")


@admin.register(Skill, site=admin_site)
class SkillAdmin(admin.ModelAdmin):
    list_display = ("name", "image_key", "image_url", "sort_order")
    search_fields = ("name", "image_key", "headline", "description")


@admin.register(Service, site=admin_site)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ("title", "slug", "starting_price", "sort_order")
    search_fields = ("title", "slug", "description", "overview")


@admin.register(ServiceRequest, site=admin_site)
class ServiceRequestAdmin(admin.ModelAdmin):
    list_display = ("service", "requester", "status", "created_at")
    list_filter = ("status", "service")
    search_fields = (
        "service__title",
        "requester__username",
        "requester__email",
        "message",
    )


@admin.register(ContactGroup, site=admin_site)
class ContactGroupAdmin(admin.ModelAdmin):
    list_display = ("title", "sort_order")
    search_fields = ("title",)


@admin.register(ContactLink, site=admin_site)
class ContactLinkAdmin(admin.ModelAdmin):
    list_display = ("label", "group", "icon", "sort_order")
    list_filter = ("group",)
    search_fields = ("label", "url", "icon")


@admin.register(GalleryPhoto, site=admin_site)
class GalleryPhotoAdmin(admin.ModelAdmin):
    list_display = ("title", "site_content", "image_url", "sort_order")
    list_filter = ("site_content",)
    search_fields = ("title", "image_url", "caption")


class ContactMessageInline(admin.TabularInline):
    model = ContactMessage
    extra = 1
    fields = ("sender", "content", "created_at")
    readonly_fields = ("created_at",)


@admin.register(ContactThread, site=admin_site)
class ContactThreadAdmin(admin.ModelAdmin):
    list_display = ("subject", "requester", "status", "last_message_at", "updated_at")
    list_filter = ("status",)
    search_fields = ("subject", "requester__username", "requester__email", "messages__content")
    inlines = [ContactMessageInline]

    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        for instance in instances:
            if isinstance(instance, ContactMessage) and not instance.sender_id:
                instance.sender = request.user
            instance.save()
            if isinstance(instance, ContactMessage):
                thread = instance.thread
                thread.status = ContactThread.Status.REPLIED if request.user.is_staff else ContactThread.Status.OPEN
                thread.last_message_at = timezone.now()
                thread.save(update_fields=["status", "last_message_at", "updated_at"])
        formset.save_m2m()
