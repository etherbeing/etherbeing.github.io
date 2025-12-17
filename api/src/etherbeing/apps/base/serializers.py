from rest_framework.serializers import ModelSerializer, Serializer
from .models import BlogEntry, Project, BlogEntryComment

class PostSerializer(Serializer):
    pass

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
