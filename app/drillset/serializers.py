"""
Serializers for drillset API.
"""
from rest_framework import serializers

from core.models import DrillSet, Drill


class DrillSetSerializer(serializers.ModelSerializer):
    """Serializer for DrillSet objects"""
    drills = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Drill.objects.all()
    )  # Allow specifying drills by their IDs

    class Meta:
        model = DrillSet
        fields = ['id', 'name', 'drills', 'createdBy']
        read_only_fields = ['id', 'createdBy']

    def create(self, validated_data):
        drills = validated_data.pop('drills', [])
        drillset = DrillSet.objects.create(**validated_data)
        drillset.drills.set(drills)
        return drillset

    def update(self, instance, validated_data):
        drills = validated_data.pop('drills', None)
        if drills is not None:
            instance.drills.set(drills)
        return super().update(instance, validated_data)
