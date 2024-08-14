from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import (
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
    AllowAny
)

from core.models import DrillSet
from drillset import serializers


class DrillSetViewSet(viewsets.ModelViewSet):
    """View for managing drillset APIs"""
    serializer_class = serializers.DrillSetSerializer
    queryset = DrillSet.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]
    authentication_classes = [TokenAuthentication]

    def get_queryset(self):
        """Return all objects"""
        return self.queryset.order_by('-id')

    def get_permissions(self):
        """Customize permissions based on action."""
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            self.permission_classes = [IsAuthenticated]
        elif self.action in ['retrieve', 'list']:
            self.permission_classes = [AllowAny]
        return super().get_permissions()

    def perform_create(self, serializer):
        """Create a new drillset and assign the createdBy field"""
        serializer.save(createdBy=self.request.user)

    @action(
        detail=False,
        methods=['get'],
        url_path=r'by_user/(?P<user_id>\d+)',
        url_name='by_user'
    )
    def by_user(self, request, user_id=None):
        """Retrieve drillsets by user"""
        drillsets = self.queryset.filter(createdBy=user_id)
        serializer = self.get_serializer(drillsets, many=True)
        return Response(serializer.data)