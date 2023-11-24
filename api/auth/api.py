from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.authtoken.models import Token
from rest_framework import status, viewsets, filters
from rest_framework.generics import GenericAPIView, get_object_or_404
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_registration.utils.responses import get_ok_response

from api.mixins import PaginationBreaker, UltraModelViewSet
from .serializers import LoginSerializer, UserSerializer, ProfileSerializer, RegisterUserSerializer, \
    ResetPasswordSerializer, SendResetPasswordKeySerializer, ChangePasswordSerializer, ReadClientSerializer, \
    ClientSerializer
from account.models import User, UserResetPassword, Client

from .services import UserPasswordResetManager
from ..paginations import StandardResultsSetPagination
from ..permissions import IsSuperAdmin


class LoginApiView(GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        login_serializer = self.serializer_class(data=request.data)
        login_serializer.is_valid(raise_exception=True)
        user = authenticate(username=request.data['username'], password=request.data['password'])
        if user:
            serializer = UserSerializer(user, many=False, context={'request': request})
            token = Token.objects.get_or_create(user=user)[0].key
            data = {**serializer.data, 'token': f'{token}'}
            return Response(data, status.HTTP_200_OK)
        return Response({'login': _('Не существует пользователя или неверный пароль')},
                        status.HTTP_400_BAD_REQUEST)


class RegisterApiView(GenericAPIView):

    serializer_class = RegisterUserSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        response_serializer = UserSerializer(user, many=False, context={'request': request})
        token = Token.objects.get_or_create(user=user)[0].key
        data = {**response_serializer.data, 'token': f'{token}'}
        return Response(data, status.HTTP_201_CREATED)


class ProfileApiView(GenericAPIView):
    queryset = User.objects.all()
    serializer_class = ProfileSerializer
    response_serializer = UserSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        return self.profile_response(request, request.user)
    
    def profile_response(self, request, user):
        serializer = self.response_serializer(user, many=False, context={'request': request})
        return Response(serializer.data)

    def patch(self, request, *args, **kwargs):
        serializer = self.serializer_class(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        return self.profile_response(request, instance)


class UserViewSet(PaginationBreaker, viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend,
                       filters.OrderingFilter,
                       filters.SearchFilter]
    ordering_fields = ['created_at']
    search_fields = ['phone', 'first_name', 'last_name', 'email', 'username']
    permission_classes = (IsAuthenticated,)


class ChangePasswordApiView(GenericAPIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = request.user
        user.set_password(serializer.validated_data['password'])
        user.save()
        return get_ok_response(_('Пароль успешно изменен'))


class SendResetPasswordKeyApiView(GenericAPIView):
    serializer_class = SendResetPasswordKeySerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        user = get_object_or_404(User, email=email)
        manager = UserPasswordResetManager(user)
        manager.send_key()
        return get_ok_response(_('Ключ успешно отправлен'))


class ResetPasswordByKeyApiView(GenericAPIView):
    serializer_class = ResetPasswordSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        key = serializer.validated_data['key']
        new_password = serializer.validated_data['new_password']
        reset_password = get_object_or_404(UserResetPassword, key=key)
        manager = UserPasswordResetManager(reset_password.user)
        is_changed = manager.reset_password(new_password, key)
        return Response(
            {'is_changed': is_changed},
            status=status.HTTP_200_OK if is_changed else status.HTTP_400_BAD_REQUEST
        )


class ClientViewSet(UltraModelViewSet):
    queryset = Client.objects.all()
    serializer_classes = {
        'create': ClientSerializer,
        'list': ReadClientSerializer,
        'update': ClientSerializer,
        'retrieve': ReadClientSerializer,
    }
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend,
                       filters.OrderingFilter,
                       filters.SearchFilter]
    ordering_fields = ['created_at']
    filterset_fields = ['user']
    permission_classes_by_action = {
        'create': (AllowAny,),
        'list': (IsAuthenticated, IsSuperAdmin,),
        'update': (IsAuthenticated, IsSuperAdmin,),
        'retrieve': (IsAuthenticated, IsSuperAdmin),
        'destroy': (IsAuthenticated, IsSuperAdmin),
    }