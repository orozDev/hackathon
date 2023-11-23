from rest_framework import routers
from django.urls import path, include
from .yasg import urlpatterns as url_doc
from . import api

router = routers.DefaultRouter()

urlpatterns = [
    path('auth/', include('api.auth.endpoints')),
    path('', include(router.urls)),
]

urlpatterns += url_doc
