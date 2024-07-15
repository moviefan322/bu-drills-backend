"""
Views for DrillScoreAPIs.
"""
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import DrillScore
from drillScore import serializers


class DrillScoreViewSet(viewsets.ModelViewSet):
    """View for manage drillScore APIs"""
    serializer_class = serializers.DrillScoreSerializer
    queryset = DrillScore.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Return objects for the current authenticated user only"""
        return self.queryset.filter(user=self.request.user).order_by('-id')
