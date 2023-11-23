from django.urls import path, include
from rest_framework import routers
from . import api

router = routers.DefaultRouter()
router.register('users', api.UserViewSet)

urlpatterns = [
    path('profile/', api.ProfileApiView.as_view()),
    path('login/', api.LoginApiView.as_view()),
    path('register/', api.RegisterApiView.as_view()),
    path('change_password/', api.ChangePasswordApiView.as_view()),
    path('send_reset_password_key/', api.SendResetPasswordKeyApiView.as_view()),
    path('reset_password_by_key/', api.ResetPasswordByKeyApiView.as_view()),
    path('', include(router.urls)),
]
