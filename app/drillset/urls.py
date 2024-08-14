"""
URL mappings from the drillset app.
"""

from django.urls import (
    path,
    include
)

from rest_framework.routers import DefaultRouter

from drillset import views

router = DefaultRouter()
router.register('', views.DrillSetViewSet)

app_name = 'drillset'

urlpatterns = [
    path('', include(router.urls)),
]