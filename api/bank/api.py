from api.bank.serializers import BranchSerializer, ReadBranchSerializer, BranchScheduleSerializer
from api.mixins import UltraModelViewSet
from api.paginations import StandardResultsSetPagination
from api.permissions import IsSuperAdmin
from bank.models import Branch, BranchSchedule
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.permissions import IsAuthenticated, AllowAny


class BranchViewSet(UltraModelViewSet):
    queryset = Branch.objects.all()
    serializer_classes = {
        'create': ReadBranchSerializer,
        'list': BranchSerializer,
        'update': ReadBranchSerializer,
        'retrieve': BranchSerializer,
    }
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend,
                       filters.OrderingFilter,
                       filters.SearchFilter]
    ordering_fields = ['created_at']
    filterset_fields = ['city']
    permission_classes_by_action = {
        'create': (IsAuthenticated, IsSuperAdmin,),
        'list': (AllowAny,),
        'update': (IsAuthenticated, IsSuperAdmin,),
        'retrieve': (AllowAny,),
        'destroy': (IsAuthenticated, IsSuperAdmin),
    }


class BranchScheduleViewSet(UltraModelViewSet):
    queryset = BranchSchedule.objects.all()
    serializer_class = BranchScheduleSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend,
                       filters.OrderingFilter,
                       filters.SearchFilter]
    ordering_fields = ['created_at']
    filterset_fields = ['branch', 'day']
    permission_classes_by_action = {
        'create': (IsAuthenticated, IsSuperAdmin,),
        'list': (AllowAny,),
        'update': (IsAuthenticated, IsSuperAdmin,),
        'retrieve': (AllowAny,),
        'destroy': (IsAuthenticated, IsSuperAdmin),
    }