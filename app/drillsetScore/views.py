from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import DrillSetScore
from drillsetScore import serializers
from .permissions import IsOwner 

class DrillSetScoreViewSet(viewsets.ModelViewSet):
    """View for managing drillSetScore APIs"""
    serializer_class = serializers.DrillSetScoreSerializer
    queryset = DrillSetScore.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsOwner] 

    def get_queryset(self):
        """Return objects for the current authenticated user only"""
        return self.queryset.filter(user=self.request.user).order_by('-id')

    def perform_create(self, serializer):
        """Create a new drillSetScore"""
        serializer.save(user=self.request.user)
