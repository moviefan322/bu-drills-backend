"""
Serializers for drillScore API.
"""
from rest_framework import serializers

from core.models import DrillScore


class DrillScoreSerializer(serializers.ModelSerializer):
    """Serializer for drillScore objects"""

    class Meta:
        model = DrillScore
        fields = ['id', 'user', 'drillId', 'score', 'maxScore', 'createdAt']
        read_only_fields = ['id', 'user']


class DrillScoreDetailSerializer(DrillScoreSerializer):
    """Serialize a drillScore detail"""

    class Meta(DrillScoreSerializer.Meta):
        fields = DrillScoreSerializer.Meta.fields
        read_only_fields = DrillScoreSerializer.Meta.read_only_fields
