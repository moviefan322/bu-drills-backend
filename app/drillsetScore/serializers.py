from rest_framework import serializers
from core.models import DrillScore, DrillSet, DrillSetScore

class DrillSetScoreSerializer(serializers.ModelSerializer):
    """Serializer for DrillSetScore objects"""
    drill_set = serializers.PrimaryKeyRelatedField(queryset=DrillSet.objects.all())
    scores = serializers.PrimaryKeyRelatedField(many=True, queryset=DrillScore.objects.all())

    class Meta:
        model = DrillSetScore
        fields = ['id', 'drill_set', 'scores', 'created_at']
        read_only_fields = ['id', 'created_at', 'user']

    def create(self, validated_data):
        scores = validated_data.pop('scores', [])
        drill_set_score = DrillSetScore.objects.create(**validated_data)
        drill_set_score.scores.set(scores)
        return drill_set_score

    def update(self, instance, validated_data):
        scores = validated_data.pop('scores', None)
        if scores is not None:
            instance.scores.set(scores)
        return super().update(instance, validated_data)
