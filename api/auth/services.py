from django.core.mail import send_mail
from django.utils.html import strip_tags

from account.models import User, UserResetPassword
from django.conf import settings
from urllib.parse import urlencode


class UserPasswordResetManager:

    def __init__(self, user: User):
        self.user = user

    def _get_password_reset(self):
        return UserResetPassword.objects.get_or_create(user=self.user)[0]

    def _make_link(self, password_reset: UserResetPassword) -> str:
        host = settings.FRONTEND_HOST
        link = settings.FRONTED_RESET_PASSWORD_LINK
        field_name = settings.QUERY_FIELD_NAME_RP
        return f'{host}{link}?{urlencode({field_name: password_reset.key})}'

    def send_key(self):
        password_reset = self._get_password_reset()
        link = self._make_link(password_reset)
        subject, from_email, to = 'Oroz.com | Reset Password', settings.EMAIL_HOST_USER, self.user.email
        html_message = f'Your link to reset password <a href="{link}">here</a>'
        plain_message = strip_tags(html_message)
        send_mail(subject, plain_message, from_email, [to], html_message=html_message)

    def reset_password(self, new_password, key):
        password_reset = self._get_password_reset()
        if password_reset.key == key:
            self.user.set_password(new_password)
            self.user.save()
            password_reset.delete()
            return True
        return False
