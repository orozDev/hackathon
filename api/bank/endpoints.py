from django.urls import path, include
from . import api
from rest_framework import routers

router = routers.DefaultRouter()
router.register('branches', api.BranchViewSet)
router.register('branch-schedules', api.BranchScheduleViewSet)

urlpatterns = [
    path('', include(router.urls))
]