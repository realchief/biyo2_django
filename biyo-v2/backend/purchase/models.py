from django.db import models
from django.utils.translation import ugettext_lazy as _
from employees.models import Employee
from products.models import Product
from django.core.urlresolvers import reverse


class Purchase(models.Model):
    STATUSES = (
        ('draft', _('Draft')),
        ('shipped', _('Shipped')),
        ('accepted', _('Accepted')),
        ('deleted', _('Deleted'))
    )

    document_number = models.CharField(_('Document number'), max_length=200, null=True, blank=True)
    status = models.CharField(_('Status'), choices=STATUSES, max_length=10, default='draft')
    note = models.TextField(_('Note'), null=True, blank=True)

    employee_created = models.ForeignKey(Employee,
                                         verbose_name=_('Employee that created the order'),
                                         related_name='purchase_created')
    employee_update = models.ForeignKey(Employee,
                                        verbose_name=_('Employee that update the order'),
                                        related_name='purchase_updated',
                                        null=True)

    shipped_dt = models.DateTimeField(_('Shipped date'), null=True)
    accepted_dt = models.DateTimeField(_('Accepted date'), null=True)
    created_dt = models.DateTimeField(_('Created date'), auto_now_add=True)

    def get_absolute_url(self):
        return reverse('quick:order_%s' % self.status, kwargs={'pk': self.id})


class PurchaseItem(models.Model):
    purchase = models.ForeignKey(Purchase, verbose_name=_('Purchase'), related_name='purchase_items')
    product = models.ForeignKey(Product, verbose_name=_('Product'), null=True)

    entered_stock = models.DecimalField(_('Entered stock'),
                                        decimal_places=2, max_digits=20)
    accepted_stock = models.DecimalField(_('Accepted stock'),
                                         decimal_places=2, max_digits=20, null=True)
    scan_dt = models.DateTimeField(_('Scan date'), null=True)
    is_deleted = models.BooleanField(_('Is deleted'), default=False)


    @property
    def difference_stock(self):
        return self.accepted_stock - self.entered_stock

    @property
    def total(self):
        return self.accepted_stock + self.product.stock

