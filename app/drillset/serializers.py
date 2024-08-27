from rest_framework import serializers
from core.models import DrillSet, Drill, DrillSetMembership
from drill.serializers import TableSetupSerializer


class DrillSerializer(serializers.ModelSerializer):
    """Serializer for Drill objects"""
    tableSetup = TableSetupSerializer()

    class Meta:
        model = Drill
        fields = '__all__'


class DrillSetSerializer(serializers.ModelSerializer):
    """Serializer for DrillSet objects"""
    drills = serializers.SerializerMethodField()

    class Meta:
        model = DrillSet
        fields = ['id', 'name', 'drills', 'createdBy']
        read_only_fields = ['id', 'createdBy']

    def get_drills(self, obj):
        # Ensure that the DrillSerializer is being used correctly
        memberships = DrillSetMembership.objects.filter(drill_set=obj).order_by('position')
        drills = [membership.drill for membership in memberships]
        return DrillSerializer(drills, many=True).data

    def create(self, validated_data):
        drills = validated_data.pop('drills', [])
        drillset = DrillSet.objects.create(**validated_data)
        for index, drill in enumerate(drills):
            DrillSetMembership.objects.create(
                drill=drill,
                drill_set=drillset,
                position=index + 1  # Positions are 1-based
            )
        return drillset

    def update(self, instance, validated_data):
        drills = validated_data.pop('drills', None)
        if drills is not None:
            # Clear existing memberships
            DrillSetMembership.objects.filter(drill_set=instance).delete()
            # Create new memberships with updated drills
            for index, drill in enumerate(drills):
                DrillSetMembership.objects.create(
                    drill=drill,
                    drill_set=instance,
                    position=index + 1
                )
        return super().update(instance, validated_data)
