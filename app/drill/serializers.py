from rest_framework import serializers
from core.models import Drill
import json

from rest_framework import serializers
from core.models import Drill, Skill


class SkillSerializer(serializers.ModelSerializer):
    """Serializer for skill objects"""

    class Meta:
        model = Skill
        fields = ['id', 'name']
        read_only_fields = ['id']


class DrillSerializer(serializers.ModelSerializer):
    """Serializer for drill objects"""
    skills = SkillSerializer(many=True, required=False)

    class Meta:
        model = Drill
        fields = [
            'id', 'name', 'maxScore', 'instructions', 'image',
            'type', 'skills', 'attempts', 'layouts', 'layoutMaxScore'
        ]
        read_only_fields = ['id', 'createdAt', 'uploadedBy']

    def _get_or_create_skills(self, skills, drill):
        """Handle getting or creating skills as needed"""
        for skill in skills:
            skill_obj, created = Skill.objects.get_or_create(**skill)
            drill.skills.add(skill_obj)

    def create(self, validated_data):
        """Create a drill."""
        skills = validated_data.pop('skills', [])
        drill = Drill.objects.create(**validated_data)
        self._get_or_create_skills(skills, drill)
        return drill

    def update(self, instance, validated_data):
        """Update a drill."""
        skills = validated_data.pop('skills', None)
        if skills is not None:
            instance.skills.clear()
            self._get_or_create_skills(skills, instance)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance



class DrillDetailSerializer(DrillSerializer):
    """Serialize a drill detail"""

    class Meta(DrillSerializer.Meta):
        fields = DrillSerializer.Meta.fields
        read_only_fields = DrillSerializer.Meta.read_only_fields