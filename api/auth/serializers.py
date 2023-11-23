from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from account.models import User


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
            'username',
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
        user = User.objects.create(**validated_data)
        user.set_password(validated_data['password'])
        user.save()

        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


class UserSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    get_full_name = serializers.CharField(read_only=True)

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