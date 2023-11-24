from uuid import uuid4

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django_resized import ResizedImageField
from phonenumber_field.modelfields import PhoneNumberField

from utils.models import TimeStampAbstractModel
from .managers import UserManager


class User(AbstractUser):

    CLIENT = 'client'
    STAFF = 'staff'
    ADMIN = 'admin'

    ROLE = (
        (CLIENT, _('Клиент')),
        (STAFF, _('Сотрудник')),
        (ADMIN, _('Администратор')),
    )

    class Meta:
        verbose_name = _('пользователь')
        verbose_name_plural = _('пользователи')
        ordering = ('-date_joined',)

    username = None
    avatar = ResizedImageField(size=[500, 500], crop=['middle', 'center'],
                               upload_to='avatars/', force_format='WEBP', quality=90, verbose_name=_('аватарка'),
                               null=True, blank=True)
    phone = PhoneNumberField(max_length=100, unique=True, verbose_name=_('номер телефона'))
    email = models.EmailField(blank=True, verbose_name=_('электронная почта'), unique=True)
    role = models.CharField(_('роль'), choices=ROLE, default=CLIENT, max_length=10)
    last_activity = models.DateTimeField(blank=True,
                                         null=True, verbose_name=_('последнее действие'), )

    objects = UserManager()

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []

    @property
    def get_full_name(self):
        return f'{self.last_name} {self.first_name}'

    get_full_name.fget.short_description = _('полное имя')

    def __str__(self):
        return f'{self.get_full_name or str(self.phone)}'


def get_expire_date():
    return timezone.now() + timezone.timedelta(days=settings.EXPIRE_DAYS)


class UserResetPassword(TimeStampAbstractModel):
    class Meta:
        verbose_name = _('Ключ для сброса пароля')
        verbose_name_plural = _('Ключи для сброса пароля')
        ordering = ('-created_at', '-updated_at')

    user = models.OneToOneField('account.User', on_delete=models.CASCADE, verbose_name=_('пользователь'))
    key = models.UUIDField(_('ключ'), default=uuid4, editable=False)
    expire_date = models.DateTimeField(_('срок действия'),
                                       default=get_expire_date)

    def __str__(self):
        return f'{self.user}'


class Client(TimeStampAbstractModel):

    SIMPLE = 'simple'
    PLATINUM = 'platinum'
    GOLD = 'gold'

    STATUS = (
        (SIMPLE, _('Simple')),
        (PLATINUM, _('Platinum')),
        (GOLD, _('Gold')),
    )

    class Meta:
        verbose_name = _('клиент')
        verbose_name_plural = _('клиенты')
        ordering = ('-created_at', '-updated_at')

    user = models.OneToOneField('account.User', models.CASCADE, related_name='client', verbose_name=_('пользователь'))
    status = models.CharField(_('статус'), max_length=10, choices=STATUS, default=SIMPLE)


class Staff(TimeStampAbstractModel):

    class Meta:
        verbose_name = _('сотрудник')
        verbose_name_plural = _('сотрудники')
        ordering = ('-created_at', '-updated_at')

    user = models.OneToOneField('account.User', models.CASCADE, related_name='staff', verbose_name=_('пользователь'))
    branch = models.ForeignKey('bank.Branch', models.PROTECT, verbose_name=_('место работы'))

    def __str__(self):
        return f'{self.user.get_full_name} - {self.branch}'

# Create your models here.
