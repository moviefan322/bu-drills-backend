"""
Serializers for drill API.
"""
from rest_framework import serializers

from core.models import Drill

import json


class DrillSerializer(serializers.ModelSerializer):
    """Serializer for drill objects"""

    class Meta:
        model = Drill
        fields = [
            'id', 'name', 'maxScore', 'instructions', 'image',
            'type', 'skills', 'attempts', 'layouts',
            'layoutMaxScore']
        read_only_fields = ['id', 'createdAt', 'uploadedBy']

    def validate_skills(self, value):
        """Ensure that skills is always handled as a JSON list"""
        if isinstance(value, str):
            try:
                value = json.loads(value)
            except json.JSONDecodeError:
                raise serializers.ValidationError(
                    "Skills must be a valid JSON list"
                    )
        return value


class DrillDetailSerializer(DrillSerializer):
    """Serialize a drill detail"""

    class Meta(DrillSerializer.Meta):
        fields = DrillSerializer.Meta.fields
        read_only_fields = DrillSerializer.Meta.read_only_fields
