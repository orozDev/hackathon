from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from bank.models import BranchSchedule, Branch, Record, RecordToStaff, Queue


class BranchScheduleStackedInline(admin.StackedInline):
    model = BranchSchedule
    extra = 0


@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = ('id', 'city', 'address',)
    list_display_links = ('id', 'city',)
    list_filter = ('city',)
    search_fields = ('name',)
    readonly_fields = ('created_at', 'updated_at',)
    inlines = (BranchScheduleStackedInline,)


@admin.register(Record)
class RecordAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'branch', 'meeting_date', 'status')
    list_display_links = ('id', 'name',)
    list_filter = ('user', 'service', 'status', 'branch', 'meeting_date',)
    search_fields = ('name', 'code',)
    readonly_fields = ('created_at', 'updated_at',)


@admin.register(RecordToStaff)
class RecordToStaffAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'staff', 'meeting_date', 'status')
    list_display_links = ('id', 'name',)
    list_filter = ('user', 'status', 'staff', 'meeting_date',)
    search_fields = ('name', 'code',)
    readonly_fields = ('created_at', 'updated_at',)


@admin.register(Queue)
class QueueAdmin(admin.ModelAdmin):
    list_display = ('id', 'slug', 'branch', 'created_at', 'status',)
    list_display_links = ('id', 'slug',)
    list_filter = ('branch', 'service', 'status',)
    readonly_fields = ('created_at', 'updated_at',)

    @admin.display(description=_('номер'))
    def slug(self, obj: Queue):
        return obj.slug

# Register your models here.
