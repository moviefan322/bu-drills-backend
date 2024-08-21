"""
URL mappings from the drill app.
"""
from django.urls import (
    path,
    include
)

from rest_framework.routers import DefaultRouter

from drill import views

router = DefaultRouter()
router.register('drills', views.DrillViewSet)
router.register('table-setups', views.TableSetupViewSet)

app_name = 'drill'

urlpatterns = [
    path('', include(router.urls)),
]
