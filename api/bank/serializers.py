from datetime import datetime

from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from django.utils import timezone
from api.serializers import CitySerializer, ServiceSerializer
from bank.models import Branch, BranchSchedule, Record, Queue
from utils.serializers import ShortDescUserSerializer


class ScheduleForBranchSerializer(serializers.ModelSerializer):
    class Meta:
        model = BranchSchedule
        exclude = ('branch',)


class ReadBranchSerializer(serializers.ModelSerializer):
    city = CitySerializer()
    schedules = ScheduleForBranchSerializer(many=True)
    is_open = serializers.BooleanField()

    class Meta:
        model = Branch
        fields = '__all__'


class BranchSerializer(serializers.ModelSerializer):
    schedules = ScheduleForBranchSerializer(many=True)

    class Meta:
        model = Branch
        fields = '__all__'

    def create(self, validated_data):
        schedules = validated_data.pop('schedules', [])
        branch = super().create(validated_data)
        for schedule in schedules:
            BranchSchedule.objects.create(**schedule, branch=branch)
        return branch


class BranchScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = BranchSchedule
        fields = '__all__'


class CreateRecordSerializer(serializers.ModelSerializer):
    user = serializers.CurrentUserDefault()

    class Meta:
        model = Record
        exclude = ('code', 'user',)

    def validate(self, attrs):
        branch = attrs.get('branch')
        meeting_date = attrs.get('meeting_date')
        service = attrs.get('service')
        if not branch.is_open:
            raise serializers.ValidationError({'branch': [_('Отделение закрыто')]})
        record = Record.objects.filter(
            branch=branch,
            meeting_date=meeting_date,
            service=service,
            status=Record.WAITING,
        )
        if record.exists():
            raise serializers.ValidationError({'branch': [
                _(f'{meeting_date.date()} в {meeting_date.time()} в отделение уже есть запись')]})
        return attrs


class ReadBranchForRecordSerializer(serializers.ModelSerializer):
    city = CitySerializer()
    is_open = serializers.BooleanField()

    class Meta:
        model = Branch
        fields = '__all__'


class ReadRecordSerializer(serializers.ModelSerializer):
    user = ShortDescUserSerializer()
    branch = ReadBranchForRecordSerializer()
    service = ServiceSerializer()

    class Meta:
        model = Record
        fields = '__all__'


class UpdateRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Record
        fields = ('status',)


class CreateQueueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Queue
        fields = ('branch', 'service', 'type', 'user',)

    def create(self, validated_data):
        now = timezone.now().date()
        queues = Queue.objects.filter(created_at__date=now)
        validated_data['value'] = queues.count() + 1
        return super().create(validated_data)


class QueueSerializer(serializers.ModelSerializer):

    branch = ReadBranchForRecordSerializer()
    service = ServiceSerializer()
    user = ShortDescUserSerializer()

    class Meta:
        model = Queue
        fields = '__all__'
