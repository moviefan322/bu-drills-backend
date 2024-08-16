"""
URL mappings from the drillsetScore app.
"""

from django.urls import (
    path,
    include
)

from rest_framework.routers import DefaultRouter

from drillsetScore import views


router = DefaultRouter()
router.register('', views.DrillSetScoreViewSet)

app_name = 'drillsetScore'

urlpatterns = [
    path('', include(router.urls)),
]
