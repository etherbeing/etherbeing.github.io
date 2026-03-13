from django.conf import settings
from django.contrib import admin, messages
from django.contrib.auth import get_user_model
from django.http import HttpRequest
from django.shortcuts import redirect
from django.urls import path, reverse

from .admin_auth import (
    begin_github_login,
    finish_github_login,
    github_oauth_is_enabled,
    recaptcha_is_enabled,
    sanitize_next_url,
    verify_recaptcha_token,
)
from .forms import BootstrapSuperuserForm, RecaptchaAdminAuthenticationForm
from .models import (
    AboutHighlight,
    BlogEntry,
    BlogEntryComment,
    Configuration,
    ContactGroup,
    ContactLink,
    Project,
    Service,
    ServiceRequest,
    SiteContent,
    Skill,
    User,
)
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
        ]
        return custom_urls + urls

    def each_context(self, request):
        context = super().each_context(request)
        configuration = Configuration.get_solo()
        context.update(
            {
                "admin_favicon_url": configuration.favicon_url,
                "admin_site_name": configuration.site_name,
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
    list_display = ("gist_id", "description", "created_at", "updated_at")
    search_fields = ("gist_id", "description", "content")


@admin.register(BlogEntryComment, site=admin_site)
class BlogEntryCommentAdmin(admin.ModelAdmin):
    list_display = ("github_id", "username", "date")
    search_fields = ("github_id", "username", "content")


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
