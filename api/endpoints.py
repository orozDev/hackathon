from django.urls import path, include
from rest_framework import routers
from . import api

from .yasg import urlpatterns as url_doc

router = routers.DefaultRouter()
router.register('cities', api.CityViewSet)
router.register('services', api.ServiceViewSet)

urlpatterns = [
    path('auth/', include('api.auth.endpoints')),
    path('bank/', include('api.bank.endpoints')),
    path('', include(router.urls)),
]

urlpatterns += url_doc
