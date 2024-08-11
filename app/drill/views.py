from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny

from core.models import Drill
from drill import serializers
from drill.permissions import IsOwnerOrReadOnly


class DrillViewSet(viewsets.ModelViewSet):
    """View for managing drill APIs"""
    serializer_class = serializers.DrillDetailSerializer
    queryset = Drill.objects.all()
    permission_classes = [AllowAny]  # Allow unauthenticated access by default
    authentication_classes = [TokenAuthentication]

    def get_queryset(self):
        """Return all objects"""
        return self.queryset.order_by('-id')

    def get_serializer_class(self):
        """Return the serializer class for request."""
        if self.action == 'list':
            return serializers.DrillSerializer
        return self.serializer_class

    def get_permissions(self):
        """Customize permissions based on action."""
        if self.action in ['create']:
            self.permission_classes = [IsAuthenticated]
        if self.action in ['update', 'partial_update', 'destroy']:
            self.permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
        elif self.action == 'retrieve' or self.action == 'list':
            self.permission_classes = [AllowAny]  # Allow unauthenticated users to view details and lists
        return super().get_permissions()

    def perform_create(self, serializer):
        """Create a new drill and assign the uploadedBy field"""
        serializer.save(uploadedBy=self.request.user)

    @action(
        detail=False,
        methods=['get'],
        url_path=r'by_type/(?P<type>\w+)',
        url_name='by_type'
    )
    def by_type(self, request, type=None):
        """Retrieve drills by type"""
        drills = self.queryset.filter(type=type)
        serializer = self.get_serializer(drills, many=True)
        return Response(serializer.data)
