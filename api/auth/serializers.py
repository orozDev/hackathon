from django.contrib.auth.password_validation import validate_password
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from account.models import User, Client, Staff
from api.bank.serializers import ReadBranchSerializer
from utils.serializers import ShortDescUserSerializer


class ProfileSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = (
            'avatar',
            'username',
            'first_name',
            'last_name',
            'phone',
            'email',
        )


class RegisterUserSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = [
            'avatar',
            'first_name',
            'last_name',
            'password',
            'phone',
            'email',
        ]

        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        user = User.objects.create(**validated_data, role=User.CLIENT)
        user.set_password(validated_data['password'])
        user.save()

        return user


class LoginSerializer(serializers.Serializer):
    phone = serializers.CharField()
    password = serializers.CharField()


class ClientForUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        exclude = ('user',)


class StaffForUserSerializer(serializers.ModelSerializer):
    branch = ReadBranchSerializer()

    class Meta:
        model = Staff
        exclude = ('user',)


class UserSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    get_full_name = serializers.CharField(read_only=True)
    client = ClientForUserSerializer(read_only=True)
    staff = StaffForUserSerializer(read_only=True)

    class Meta:
        model = User
        fields = '__all__'

        extra_kwargs = {
            'password': {'write_only': True},
        }


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField()
    password = serializers.CharField()

    def validate_old_password(self, old_password):
        user = self.context['request'].user
        if not user.check_password(old_password):
            raise serializers.ValidationError(_('Старый пароль неверный'))
        return old_password

    def validate_password(self, password):
        user = self.context['request'].user
        validate_password(password, user=user)
        return password


class SendResetPasswordKeySerializer(serializers.Serializer):
    email = serializers.EmailField()


class ResetPasswordSerializer(serializers.Serializer):
    key = serializers.UUIDField()
    new_password = serializers.CharField(validators=[validate_password])


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'


class ReadClientSerializer(serializers.ModelSerializer):
    user = ShortDescUserSerializer()

    class Meta:
        model = Client
        fields = '__all__'


class StaffSerializer(serializers.ModelSerializer):
    class Meta:
        model = Staff
        fields = '__all__'


class ReadStaffSerializer(serializers.ModelSerializer):
    user = ShortDescUserSerializer()
    branch = ReadBranchSerializer()

    class Meta:
        model = Staff
        fields = '__all__'
