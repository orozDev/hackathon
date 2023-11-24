from api.bank.serializers import BranchSerializer, ReadBranchSerializer, BranchScheduleSerializer, RecordSerializer, \
    ReadRecordSerializer
from api.mixins import UltraModelViewSet
from api.paginations import StandardResultsSetPagination
from api.permissions import IsSuperAdmin
from bank.models import Branch, BranchSchedule, Record
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
    search_fields = ['address', 'description']
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
    filterset_fields = ['branch', 'week']
    permission_classes_by_action = {
        'create': (IsAuthenticated, IsSuperAdmin,),
        'list': (AllowAny,),
        'update': (IsAuthenticated, IsSuperAdmin,),
        'retrieve': (AllowAny,),
        'destroy': (IsAuthenticated, IsSuperAdmin),
    }


class RecordViewSet(UltraModelViewSet):
    queryset = Record.objects.all()
    serializer_classes = {
        'create': RecordSerializer,
        'list': ReadRecordSerializer,
        'update': RecordSerializer,
        'retrieve': ReadRecordSerializer,
    }
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend,
                       filters.OrderingFilter,
                       filters.SearchFilter]
    ordering_fields = ['created_at']
    filterset_fields = ['branch', 'service', 'user']
    search_fields = ['name']
    permission_classes_by_action = {
        'create': (IsAuthenticated,),
        'list': (AllowAny,),
        'update': (IsAuthenticated, IsSuperAdmin,),
        'retrieve': (AllowAny,),
        'destroy': (IsAuthenticated, IsSuperAdmin),
    }