from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class BankConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'bank'
    verbose_name = _('1. Электронная очередь')
