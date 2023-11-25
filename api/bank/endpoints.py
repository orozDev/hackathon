from django.urls import path, include
from . import api
from rest_framework import routers

router = routers.DefaultRouter()
router.register('branches', api.BranchViewSet)
router.register('branch-schedules', api.BranchScheduleViewSet)
router.register('records', api.RecordViewSet)
router.register('queues', api.QueueViewSet)

urlpatterns = [
    path('queue-by-record/<str:code>/', api.QueueByRecordGenericAPIView.as_view()),
    path('next-queue/', api.NextQueueGenericAPIView.as_view()),
    path('complete-queue/<int:id>/', api.CompleteQueueGenericAPIView.as_view()),
    path('', include(router.urls))
]