from api.mixins import UltraModelViewSet
from api.paginations import StandardResultsSetPagination
from api.permissions import IsSuperAdmin
from api.serializers import CitySerializer
from core.models import City
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.permissions import IsAuthenticated, AllowAny


class CityViewSet(UltraModelViewSet):
    queryset = City.objects.all()
    serializer_class = CitySerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend,
                       filters.OrderingFilter,
                       filters.SearchFilter]
    ordering_fields = ['created_at']
    search_fields = ['name']
    permission_classes_by_action = {
        'create': (IsAuthenticated, IsSuperAdmin,),
        'list': (AllowAny,),
        'update': (IsAuthenticated, IsSuperAdmin,),
        'retrieve': (AllowAny,),
        'destroy': (IsAuthenticated, IsSuperAdmin),
    }