"""
Serializers for drillScore API.
"""
from rest_framework import serializers

from core.models import DrillScore


class DrillScoreSerializer(serializers.ModelSerializer):
    """Serializer for drillScore objects"""

    class Meta:
        model = DrillScore
        fields = ('id', 'user', 'drillId', 'score', 'maxScore', 'date')
        read_only_fields = ('id', 'user')