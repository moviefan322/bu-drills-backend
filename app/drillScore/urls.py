"""
URL mappings from the drillScore app.
"""
from django.urls import (
    path,
    include
)

from rest_framework.routers import DefaultRouter

from drillScore import views


router = DefaultRouter()
router.register('', views.DrillScoreViewSet)

app_name = 'drillScore'

urlpatterns = [
    path('', include(router.urls)),
]
