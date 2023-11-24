from core.models import City, Service
from rest_framework import serializers


class CitySerializer(serializers.ModelSerializer):

    class Meta:
        model = City
        fields = '__all__'


class ServiceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Service
        fields = '__all__'
