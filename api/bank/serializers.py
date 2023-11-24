from pprint import pprint

from rest_framework import serializers
from django.utils.translation import gettext_lazy as _

from api.serializers import CitySerializer, ServiceSerializer
from bank.models import Branch, BranchSchedule, Record
from utils.models import TimeStampAbstractModel
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


class RecordSerializer(serializers.ModelSerializer):

    user = serializers.CurrentUserDefault()

    class Meta:
        model = Record
        fields = '__all__'

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