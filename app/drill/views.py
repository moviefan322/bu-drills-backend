from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response


from core.models import Drill
from drill import serializers


class DrillViewSet(viewsets.ModelViewSet):
    """View for managing drill APIs"""
    serializer_class = serializers.DrillDetailSerializer
    queryset = Drill.objects.all()

    def get_queryset(self):
        """Return all objects"""
        return self.queryset.order_by('-id')
    
    def get_serializer_class(self):
        """Return the serializer class for request."""
        if self.action == 'list':
            return serializers.DrillSerializer
        return self.serializer_class
    
    def perform_create(self, serializer):
        """Create a new drill"""
        serializer.save()

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