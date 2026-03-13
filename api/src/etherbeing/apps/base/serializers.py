from rest_framework.serializers import (
    BooleanField,
    CharField,
    ModelSerializer,
    Serializer,
    SerializerMethodField,
)

from .models import (
    AboutHighlight,
    BlogEntry,
    BlogEntryComment,
    Configuration,
    ContactGroup,
    ContactLink,
    Project,
    Service,
    SiteContent,
    Skill,
)

class PostSerializer(Serializer):
    pass


class GithubSessionSerializer(Serializer):
    is_authenticated = BooleanField()
    username = CharField(required=False, allow_blank=True)
    email = CharField(required=False, allow_blank=True)
    github_login = CharField(required=False, allow_blank=True)
    avatar_url = CharField(required=False, allow_blank=True)
    can_comment_on_gists = BooleanField(required=False)
    csrf_token = CharField()


class GithubCommentCreateSerializer(Serializer):
    content = CharField()


class ConfigurationSerializer(ModelSerializer):
    class Meta:
        model = Configuration
        fields = (
            "site_name",
            "short_name",
            "site_description",
            "favicon_url",
            "theme_color",
            "background_color",
        )


class BlogEntryCommentSerializer(ModelSerializer):
    class Meta:
        model = BlogEntryComment
        fields = "__all__"


class BlogEntrySerializer(ModelSerializer):
    comments = BlogEntryCommentSerializer(many=True)

    class Meta:
        model = BlogEntry
        fields = "__all__"


class ProjectSerializer(ModelSerializer):
    class Meta:
        model = Project
        fields = "__all__"


class AboutHighlightSerializer(ModelSerializer):
    class Meta:
        model = AboutHighlight
        fields = ("title", "content", "column", "sort_order")


class SkillSerializer(ModelSerializer):
    class Meta:
        model = Skill
        fields = ("name", "image_key", "sort_order")


class ServiceSerializer(ModelSerializer):
    class Meta:
        model = Service
        fields = ("title", "starting_price", "description", "skills", "sort_order")


class ContactLinkSerializer(ModelSerializer):
    class Meta:
        model = ContactLink
        fields = ("label", "url", "icon", "sort_order")


class ContactGroupSerializer(ModelSerializer):
    links = ContactLinkSerializer(many=True)

    class Meta:
        model = ContactGroup
        fields = ("title", "sort_order", "links")


class SiteContentSerializer(ModelSerializer):
    configuration = SerializerMethodField()
    about_highlights = AboutHighlightSerializer(many=True)
    skills = SkillSerializer(many=True)
    services = ServiceSerializer(many=True)
    contact_groups = ContactGroupSerializer(many=True)
    featured_projects = SerializerMethodField()
    featured_blog_entries = SerializerMethodField()

    class Meta:
        model = SiteContent
        fields = (
            "site_title",
            "configuration",
            "hero_titles",
            "hero_summary",
            "hero_cta_label",
            "hero_cta_url",
            "about_short_bio",
            "buy_me_a_coffee_url",
            "contact_intro",
            "footer_copy",
            "footer_tagline",
            "strategy_business_idea",
            "about_highlights",
            "skills",
            "services",
            "contact_groups",
            "featured_projects",
            "featured_blog_entries",
        )

    def get_featured_projects(self, obj: SiteContent):
        projects = Project.objects.order_by("-pushed_at", "-updated_at", "-created_at")[:5]
        return ProjectSerializer(projects, many=True).data

    def get_configuration(self, obj: SiteContent):
        return ConfigurationSerializer(Configuration.get_solo()).data

    def get_featured_blog_entries(self, obj: SiteContent):
        entries = BlogEntry.objects.order_by("-created_at")[:6]
        return BlogEntrySerializer(entries, many=True).data
