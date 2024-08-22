from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import (
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
    AllowAny
)

from core.models import Drill, TableSetup
from drill import serializers
from drill.permissions import IsOwnerOrReadOnly
from drill.serializers import DrillSerializer


class DrillViewSet(viewsets.ModelViewSet):
    """View for managing drill APIs"""
    serializer_class = serializers.DrillDetailSerializer
    queryset = Drill.objects.select_related('tableSetup').all()
    serializer_class = DrillSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]  # Default permission
    authentication_classes = [TokenAuthentication]

    def get_queryset(self):
        """Return all objects"""
        return self.queryset.order_by('-id')

    def get_permissions(self):
        """Customize permissions based on action."""
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            self.permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
        elif self.action in ['retrieve', 'list']:
            self.permission_classes = [AllowAny]
        return super().get_permissions()

    def perform_create(self, serializer):
        """Create a new drill and assign the createdBy field"""
        serializer.save(createdBy=self.request.user)

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


class TableSetupViewSet(viewsets.ModelViewSet):
    """View for managing table setup APIs"""
    serializer_class = serializers.TableSetupSerializer
    queryset = TableSetup.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]  # Default permission
    authentication_classes = [TokenAuthentication]

    def perform_create(self, serializer):
        """Create a new table setup and assign the drill if provided"""
        drill_id = self.request.data.get('drill')
        if drill_id:
            try:
                drill = Drill.objects.get(id=drill_id)
                serializer.save(drill=drill)
            except Drill.DoesNotExist:
                raise serializers.ValidationError(
                    f"Drill with id {drill_id} does not exist."
                )
        else:
            raise serializers.ValidationError("Drill ID is required.")
