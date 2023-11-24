import random
import string

from django.db import models
from django.utils.translation import gettext_lazy as _

from utils.models import TimeStampAbstractModel


class Branch(TimeStampAbstractModel):
    class Meta:
        verbose_name = _('отделение')
        verbose_name_plural = _('отделении')
        ordering = ('-created_at', '-updated_at')

    city = models.ForeignKey('core.City', models.PROTECT, verbose_name=_('город'))
    address = models.CharField(_('адрес'), max_length=100)
    description = models.TextField(_('описание'))

    def __str__(self):
        return f'{self.city} - {self.address}'


class BranchSchedule(TimeStampAbstractModel):
    MONDAY = 'monday'
    TUESDAY = 'tuesday'
    WEDNESDAY = 'wednesday'
    THURSDAY = 'thursday'
    FRIDAY = 'friday'
    SATURDAY = 'saturday'
    SUNDAY = 'sunday'

    DAYS = (
        (MONDAY, _('Понедельник')),
        (TUESDAY, _('Вторник')),
        (WEDNESDAY, _('Среда')),
        (THURSDAY, _('Четверг')),
        (FRIDAY, _('Пятница')),
        (SATURDAY, _('Суббота')),
        (SUNDAY, _('Воскресенье'))
    )

    class Meta:
        verbose_name = _('график работы банковской отделении')
        verbose_name_plural = _('графики работы банковских отделении')
        ordering = ('-created_at', '-updated_at')

    day = models.CharField(_('день'), max_length=50, choices=DAYS)
    start_time = models.TimeField(_('время открытия'))
    start_end = models.TimeField(_('время закрытия'))
    branch = models.ForeignKey('bank.Branch', models.CASCADE, 'schedules')

    def __str__(self):
        return f'{self.branch} - {self.day}'


def code_generator():
    chars = string.digits
    code = ''.join(random.choice(chars) for _ in range(10))
    return code


class Record(TimeStampAbstractModel):

    WAITING = 'waiting'
    CANCELED = 'canceled'
    COMPLETED = 'completed'

    STATUS = (
       (WAITING, _('В ожидании')),
       (CANCELED, _('Отменено')),
       (COMPLETED, _('Завершено'))
    )

    class Meta:
        verbose_name = _('запись')
        verbose_name_plural = _('записи')
        ordering = ('-created_at', '-updated_at')

    user = models.ForeignKey('account.User', models.SET_NULL, null=True, verbose_name=_('пользователь'))
    name = models.CharField(_('Имя и фамилия'), max_length=100)
    branch = models.ForeignKey('bank.Branch', models.PROTECT, verbose_name=_('отделение'))
    service = models.ForeignKey('core.Service', models.PROTECT, verbose_name=_('сервис'))
    meeting_date = models.DateTimeField(_('дата и время прихода'))
    code = models.CharField(_('код'), max_length=10, default=code_generator)
    status = models.CharField(_('статус'), max_length=20, default=WAITING, choices=STATUS)

    def __str__(self):
        return f'{self.user} - {self.branch}'


class RecordToStaff(TimeStampAbstractModel):

    WAITING = 'waiting'
    CANCELED = 'canceled'
    COMPLETED = 'completed'

    STATUS = (
       (WAITING, _('В ожидании')),
       (CANCELED, _('Отменено')),
       (COMPLETED, _('Завершено'))
    )

    class Meta:
        verbose_name = _('запись к сотруднику')
        verbose_name_plural = _('записи к сотрудникам')
        ordering = ('-created_at', '-updated_at')

    user = models.ForeignKey('account.User', models.SET_NULL, null=True, verbose_name=_('пользователь'))
    name = models.CharField(_('Имя и фамилия'), max_length=100)
    branch = models.ForeignKey('bank.Branch', models.PROTECT, verbose_name=_('отделение'))
    staff = models.ForeignKey('account.Staff', models.PROTECT, verbose_name=_('сотрудник'))
    meeting_date = models.DateTimeField(_('дата и время прихода'))
    status = models.CharField(_('статус'), max_length=20, default=WAITING, choices=STATUS)

    def __str__(self):
        return f'{self.user.get_full_name} - {self.staff.user.get_full_name}'


class Queue(TimeStampAbstractModel):

    SIMPLE = 'simple'
    RECORDED_CLIENT = 'recorded_client'

    TYPE = (
        (SIMPLE, _('обычный клиент')),
        (RECORDED_CLIENT, _('зарегистрированный клиент'))
    )

    WAITING = 'waiting'
    COMPLETED = 'completed'

    STATUS = (
        (WAITING, _('В ожидании')),
        (COMPLETED, _('Завершено'))
    )

    class Meta:
        verbose_name = _('очередь')
        verbose_name_plural = _('очереди')
        ordering = ('-created_at', '-updated_at')

    branch = models.ForeignKey('bank.Branch', models.PROTECT, verbose_name=_('отделение'))
    service = models.ForeignKey('core.Service', models.PROTECT, verbose_name=_('сервис'))
    value = models.PositiveIntegerField(_('место'))
    type = models.CharField(_('тип'), choices=TYPE, default=SIMPLE, max_length=20)
    status = models.CharField(_('статус'), choices=STATUS, default=WAITING, max_length=20)

    @property
    def slug(self):
        prefix = 'S' if self.type == self.SIMPLE else 'R'
        return f'{prefix}{self.value}'

    def __str__(self):
        return f'{self.slug} - {self.created_at}'

# Create your models here.
