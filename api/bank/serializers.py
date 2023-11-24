from rest_framework import serializers

from api.serializers import CitySerializer
from bank.models import Branch, BranchSchedule
from utils.models import TimeStampAbstractModel


class ScheduleForBranchSerializer(serializers.ModelSerializer):

    class Meta:
        model = BranchSchedule
        exclude = ('branch',)


class ReadBranchSerializer(serializers.ModelSerializer):
    city = CitySerializer()
    schedules = ScheduleForBranchSerializer(many=True)

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