from django.db import models
from django.utils.translation import gettext_lazy as _
from utils.models import TimeStampAbstractModel


class City(TimeStampAbstractModel):
    class Meta:
        verbose_name = _('город')
        verbose_name_plural = _('города')
        ordering = ('-created_at', '-updated_at')

    name = models.CharField(_('название'), max_length=100, unique=True)

    def __str__(self):
        return f'{self.name}'


class Service(TimeStampAbstractModel):
    class Meta:
        verbose_name = _('сервис')
        verbose_name_plural = _('сервисы')
        ordering = ('-created_at', '-updated_at')

    name = models.CharField(_('название'), max_length=100, unique=True)

    def __str__(self):
        return f'{self.name}'

# Create your models here.
