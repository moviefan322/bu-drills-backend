from rest_framework import serializers
from core.models import DrillScore, DrillSet, DrillSetScore


class DrillScoreSerializer(serializers.ModelSerializer):
    """Serializer for DrillScore objects"""

    class Meta:
        model = DrillScore
        fields = ['drill', 'score', 'maxScore']


class DrillSetScoreSerializer(serializers.ModelSerializer):
    """Serializer for DrillSetScore objects"""
    drill_set = serializers.PrimaryKeyRelatedField(
        queryset=DrillSet.objects.all()
    )
    scores = DrillScoreSerializer(many=True)  # Use the nested serializer

    class Meta:
        model = DrillSetScore
        fields = ['id', 'drill_set', 'scores', 'created_at']
        read_only_fields = ['id', 'created_at', 'user']

    def create(self, validated_data):
        scores_data = validated_data.pop('scores', [])
        drill_set_score = DrillSetScore.objects.create(**validated_data)
        total_score = 0
        total_max_score = 0
        for score_data in scores_data:
            newScore = DrillScore.objects.create(user=self.context['request'].user, **score_data)
            drill_set_score.scores.add(newScore)
            total_score += newScore.score
            total_max_score += newScore.maxScore

        drill_set_score.total_score = total_score
        drill_set_score.total_max_score = total_max_score
        drill_set_score.save()

        return drill_set_score

    def update(self, instance, validated_data):
        scores_data = validated_data.pop('scores', [])
        # Handle updating logic if needed
        return super().update(instance, validated_data)

