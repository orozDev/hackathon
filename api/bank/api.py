from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from django.utils.translation import gettext_lazy as _
from rest_framework.generics import GenericAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from api.bank.serializers import BranchSerializer, ReadBranchSerializer, BranchScheduleSerializer, \
    CreateRecordSerializer, \
    ReadRecordSerializer, UpdateRecordSerializer, QueueSerializer, CreateQueueSerializer
from api.mixins import UltraModelViewSet, UltraReadAndCreateModelViewSet
from api.paginations import StandardResultsSetPagination
from api.permissions import IsSuperAdmin
from bank.models import Branch, BranchSchedule, Record, Queue
from django.utils import timezone
from rest_framework.response import Response
from rest_framework import status
from django.utils.translation import gettext_lazy as _


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
        'create': CreateRecordSerializer,
        'list': ReadRecordSerializer,
        'update': UpdateRecordSerializer,
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


class QueueViewSet(UltraReadAndCreateModelViewSet):
    queryset = Queue.objects.all()
    serializer_classes = {
        'create': CreateQueueSerializer,
        'list': QueueSerializer,
        'retrieve': QueueSerializer,
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


class QueueByRecordGenericAPIView(GenericAPIView):

    serializer_class = QueueSerializer

    def get(self, request, code, *args, **kwargs):
        record = get_object_or_404(Record, code=code, status=Record.WAITING)
        now = timezone.now().date()
        queues = Queue.objects.filter(created_at__date=now)
        queue = Queue.objects.create(
            user=record.user,
            service=record.service,
            branch=record.branch,
            value=queues.count() + 1,
            type=Queue.RECORDED_CLIENT
        )
        record.status = Record.COMPLETED
        record.save()
        serializer = self.get_serializer(instance=queue)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class NextQueueGenericAPIView(GenericAPIView):

    serializer_class = QueueSerializer

    def get(self, request, *args, **kwargs):
        now = timezone.now().date()
        queue = Queue.objects.filter(created_at__date=now, status=Queue.WAITING).order_by('value')
        if queue.exists():
            queue = queue.first()
            queue.status = Queue.IN_PROGRESS
            queue.save()
            serializer = self.get_serializer(instance=queue)
            return Response(serializer.data)
        return Response(status=status.HTTP_204_NO_CONTENT)


class CompleteQueueGenericAPIView(GenericAPIView):

    serializer_class = QueueSerializer
    queryset = Queue.objects.filter(status=Queue.IN_PROGRESS)
    lookup_field = 'id'

    def get(self, request, *args, **kwargs):
        queue = self.get_object()
        queue.status = Queue.COMPLETED
        queue.save()
        serializer = self.get_serializer(instance=queue)
        return Response(serializer.data)
