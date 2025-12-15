from rest_framework.serializers import ModelSerializer, Serializer
from .models import BlogEntry, Project

class PostSerializer(Serializer):
    pass

class BlogEntrySerializer(ModelSerializer):
    class Meta:
        model = BlogEntry
        fields = "__all__"

class ProjectSerializer(ModelSerializer):
    class Meta:
        model = Project
        fields = "__all__"
