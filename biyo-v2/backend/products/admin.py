from django.contrib import admin
from . import models
from django.contrib.admin.models import LogEntry, DELETION
from django.core.urlresolvers import reverse
from django.utils.html import escape
from simple_history.admin import SimpleHistoryAdmin


class LogEntryAdmin(admin.ModelAdmin):
    date_hierarchy = 'action_time'

    readonly_fields = map(
        lambda filed_model: filed_model[0].name,
        LogEntry._meta.get_fields_with_model()
    )

    list_filter = [
        'user',
        'content_type',
        'action_flag'
    ]

    search_fields = [
        'object_repr',
        'change_message'
    ]

    list_display = [
        'action_time',
        'user',
        'content_type',
        'object_link',
        'action_flag',
        'change_message',
    ]

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser and request.method != 'POST'

    def has_delete_permission(self, request, obj=None):
        return False

    def object_link(self, obj):
        if obj.action_flag == DELETION:
            link = escape(obj.object_repr)
        else:
            ct = obj.content_type
            link = u'<a href="%s">%s</a>' % (
                reverse('admin:%s_%s_change' % (ct.app_label, ct.model), args=[obj.object_id]),
                escape(obj.object_repr),
            )
        return link

    object_link.allow_tags = True
    object_link.admin_order_field = 'object_repr'
    object_link.short_description = u'object'

    def get_queryset(self, request):
        return super(LogEntryAdmin, self).queryset(request) \
            .prefetch_related('content_type')


class ProductAdmin(SimpleHistoryAdmin):
    pass

admin.site.register(LogEntry, LogEntryAdmin)
admin.site.register(models.Product, ProductAdmin)
admin.site.register(models.Category)
admin.site.register(models.TaxRate)
admin.site.register(models.ModifierGroup)
admin.site.register(models.Modifier)
admin.site.register(models.Discount)
admin.site.register(models.Store)
admin.site.register(models.TableSection)
admin.site.register(models.Table)
admin.site.register(models.Terminal)
admin.site.register(models.Printer)
admin.site.register(models.Reward)
