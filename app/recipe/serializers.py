from core.models import Tag
from rest_framework import serializers


class TagSerializer(serializers.ModelSerializer):
    """Serializer for tag objects"""
    class Meta:
        model = Tag
        fields = ['name', 'id']
        read_only_fields = ['id']
