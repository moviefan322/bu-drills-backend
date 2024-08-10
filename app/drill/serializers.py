"""
Serializers for drill API.
"""
from rest_framework import serializers

from core.models import Drill


class DrillSerializer(serializers.ModelSerializer):
    """Serializer for drill objects"""

    class Meta:
        model = Drill
        fields = [
            'id', 'name', 'maxScore', 'instructions', 'image',
            'type', 'skills', 'attempts', 'layouts',
            'layoutMaxScore']
        read_only_fields = ['id', 'createdAt', 'uploadedBy']


class DrillDetailSerializer(DrillSerializer):
    """Serialize a drill detail"""

    class Meta(DrillSerializer.Meta):
        fields = DrillSerializer.Meta.fields
        read_only_fields = DrillSerializer.Meta.read_only_fields
