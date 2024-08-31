from rest_framework import serializers
from core.models import DrillScore, DrillSet, DrillSetScore


class DrillScoreSerializer(serializers.ModelSerializer):
    """Serializer for DrillScore objects"""

    class Meta:
        model = DrillScore
        fields = ['drill', 'score', 'maxScore', 'isSet']


class DrillSetScoreSerializer(serializers.ModelSerializer):
    drill_set = serializers.PrimaryKeyRelatedField(
        queryset=DrillSet.objects.all())
    scores = DrillScoreSerializer(many=True)  # Nested serializer for scores

    class Meta:
        model = DrillSetScore
        fields = ['id', 'drill_set', 'scores',
                  'createdAt', 'total_score', 'total_max_score']
        read_only_fields = ['id', 'createdAt', 'user']

    def create(self, validated_data):
        scores_data = validated_data.pop('scores', [])
        drill_set_score = DrillSetScore.objects.create(**validated_data)
        total_score = 0
        total_max_score = 0
        for score_data in scores_data:
            newScore = DrillScore.objects.create(
                user=self.context['request'].user,
                **score_data
            )
            newScore.isSet = True
            drill_set_score.scores.add(newScore)
            total_score += newScore.score
            total_max_score += newScore.maxScore

        drill_set_score.total_score = total_score
        drill_set_score.total_max_score = total_max_score
        drill_set_score.save()
        return drill_set_score

    def update(self, instance, validated_data):
        scores_data = validated_data.pop('scores', None)
        if scores_data is not None:
            instance.scores.clear()
            total_score = 0
            total_max_score = 0
            for score_data in scores_data:
                newScore = DrillScore.objects.create(
                    user=self.context['request'].user,
                    **score_data
                )
                instance.scores.add(newScore)
                total_score += newScore.score
                total_max_score += newScore.maxScore

            instance.total_score = total_score
            instance.total_max_score = total_max_score

        # Handle other fields
        instance.drill_set = validated_data.get(
            'drill_set',
            instance.drill_set
        )
        instance.save()
        return instance
