from django.db import models
from django.utils.translation import ugettext_lazy as _
from products.models import Terminal


class DBSettings(models.Model):
    name = models.CharField(_('Name'), max_length=50)
    value = models.CharField(_('Value'), max_length=50, null=True, blank=True)
    description = models.TextField(_('Description'), blank=True)
    terminal = models.ForeignKey(Terminal,
                                 verbose_name=_('Terminal'), null=True, blank=True)

    def __unicode__(self):
        return u'%s -> %s' % (self.name, self.value)

    class Meta:
        unique_together = (('name', 'terminal'), )
        db_table = 'settings_settings'
