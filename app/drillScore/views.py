from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

from core.models import DrillScore, Drill
from drillScore import serializers


class DrillScoreViewSet(viewsets.ModelViewSet):
    """View for managing drillScore APIs"""
    serializer_class = serializers.DrillScoreDetailSerializer
    queryset = DrillScore.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Return objects for the current authenticated user only"""
        if self.action == 'by_drill':
            return self.queryset
        return self.queryset.filter(user=self.request.user).order_by('-id')

    def get_serializer_class(self):
        """Return the serializer class for request."""
        if self.action == 'list' or self.action == 'by_drill':
            return serializers.DrillScoreSerializer
        return self.serializer_class

    def perform_create(self, serializer):
        """Create a new drillScore"""
        serializer.save(user=self.request.user)

    @action(
            detail=False,
            methods=['get'],
            url_path=r'drill/(?P<drillId>\d+)',
            url_name='by_drill'
            )
    def by_drill(self, request, drillId=None):
        """Retrieve drill scores by drill ID"""
        # Get the Drill instance by ID
        drill = get_object_or_404(Drill, id=drillId)

        # Filter scores by the drill instance
        scores = self.queryset.filter(drill=drill)

        # Serialize and return the scores
        serializer = self.get_serializer(scores, many=True)
        return Response(serializer.data)
