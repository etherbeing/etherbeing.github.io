from rest_framework.serializers import (
    BooleanField,
    CharField,
    ModelSerializer,
    Serializer,
    SerializerMethodField,
    ChoiceField,
)

from .models import (
    AboutHighlight,
    BlogEntry,
    BlogEntryComment,
    Configuration,
    ContactGroup,
    ContactLink,
    ContactMessage,
    ContactThread,
    GalleryPhoto,
    Project,
    Service,
    ServiceRequest,
    SiteContent,
    Skill,
    User,
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
    recaptcha_enabled = BooleanField(required=False)
    recaptcha_site_key = CharField(required=False, allow_blank=True)
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
        fields = ("name", "image_key", "image_url", "headline", "description", "sort_order")


class ServiceSerializer(ModelSerializer):
    class Meta:
        model = Service
        fields = (
            "slug",
            "title",
            "headline",
            "starting_price",
            "description",
            "overview",
            "skills",
            "deliverables",
            "process_steps",
            "outcomes",
            "engagement_cta",
            "sort_order",
        )


class ServiceRequestCreateSerializer(Serializer):
    message = CharField(required=False, allow_blank=True)


class ServiceRequesterSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "email", "github_login")


class ServiceRequestSerializer(ModelSerializer):
    service = ServiceSerializer()
    requester = ServiceRequesterSerializer()
    status = ChoiceField(choices=ServiceRequest.Status.choices)

    class Meta:
        model = ServiceRequest
        fields = (
            "id",
            "service",
            "requester",
            "status",
            "message",
            "created_at",
            "updated_at",
        )


class ContactMessageSerializer(ModelSerializer):
    sender_username = SerializerMethodField()
    is_staff_reply = SerializerMethodField()

    class Meta:
        model = ContactMessage
        fields = (
            "id",
            "sender_username",
            "is_staff_reply",
            "content",
            "created_at",
        )

    def get_sender_username(self, obj: ContactMessage):
        return obj.sender.username

    def get_is_staff_reply(self, obj: ContactMessage):
        return obj.sender.is_staff


class ContactThreadSerializer(ModelSerializer):
    messages = ContactMessageSerializer(many=True)

    class Meta:
        model = ContactThread
        fields = (
            "id",
            "subject",
            "status",
            "created_at",
            "updated_at",
            "last_message_at",
            "messages",
        )


class ContactThreadCreateSerializer(Serializer):
    subject = CharField()
    content = CharField()
    recaptcha_token = CharField(required=False, allow_blank=True)


class ContactMessageCreateSerializer(Serializer):
    content = CharField()
    recaptcha_token = CharField(required=False, allow_blank=True)


class ContactLinkSerializer(ModelSerializer):
    class Meta:
        model = ContactLink
        fields = ("label", "url", "icon", "sort_order")


class ContactGroupSerializer(ModelSerializer):
    links = ContactLinkSerializer(many=True)

    class Meta:
        model = ContactGroup
        fields = ("title", "sort_order", "links")


class GalleryPhotoSerializer(ModelSerializer):
    class Meta:
        model = GalleryPhoto
        fields = ("title", "image_url", "caption", "sort_order")


class SiteContentSerializer(ModelSerializer):
    configuration = SerializerMethodField()
    about_highlights = AboutHighlightSerializer(many=True)
    skills = SkillSerializer(many=True)
    services = ServiceSerializer(many=True)
    contact_groups = ContactGroupSerializer(many=True)
    gallery_photos = GalleryPhotoSerializer(many=True)
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
            "featured_chart_symbol",
            "featured_chart_title",
            "strategy_business_idea",
            "about_highlights",
            "skills",
            "services",
            "contact_groups",
            "gallery_photos",
            "featured_projects",
            "featured_blog_entries",
        )

    def get_featured_projects(self, obj: SiteContent):
        projects = Project.objects.order_by("-pushed_at", "-updated_at", "-created_at")[:5]
        return ProjectSerializer(projects, many=True).data

    def get_configuration(self, obj: SiteContent):
        return ConfigurationSerializer(Configuration.get_solo()).data

    def get_featured_blog_entries(self, obj: SiteContent):
        entries = BlogEntry.objects.filter(hide_from_web=False).order_by("-created_at")[:6]
        return BlogEntrySerializer(entries, many=True).data
