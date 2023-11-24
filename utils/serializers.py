from rest_framework import serializers

from account.models import User


class ShortDescUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'avatar',
            'email',
            'phone',
            'first_name',
            'last_name',
            'role',
        )